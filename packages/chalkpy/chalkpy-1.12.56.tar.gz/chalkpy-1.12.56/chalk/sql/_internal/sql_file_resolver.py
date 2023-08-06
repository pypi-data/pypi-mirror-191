from __future__ import annotations

import dataclasses
import inspect
import json
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterable, List, Literal, Optional, Type, Union, cast

import yaml
from pydantic import BaseModel, ValidationError, validator

from chalk import OfflineResolver, OnlineResolver
from chalk.features import DataFrame, Feature, Features
from chalk.features.resolver import ResolverArgErrorHandler, StreamResolver
from chalk.sql import TableIngestProtocol
from chalk.sql._internal.integrations.bigquery import BigQuerySourceImpl
from chalk.sql._internal.integrations.cloudsql import CloudSQLSourceImpl
from chalk.sql._internal.integrations.mysql import MySQLSourceImpl
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.sql._internal.integrations.redshift import RedshiftSourceImpl
from chalk.sql._internal.integrations.snowflake import SnowflakeSourceImpl
from chalk.sql._internal.integrations.sqlite import SQLiteFileSourceImpl
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.streams import KafkaSource
from chalk.streams.base import StreamSource
from chalk.streams.types import StreamResolverSignature
from chalk.utils.duration import parse_chalk_duration
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlglot.expressions import Expression

_SOURCES = {
    "snowflake": SnowflakeSourceImpl,
    "postgres": PostgreSQLSourceImpl,
    "postgresql": PostgreSQLSourceImpl,
    "mysql": MySQLSourceImpl,
    "bigquery": BigQuerySourceImpl,
    "cloudsql": CloudSQLSourceImpl,
    "redshift": RedshiftSourceImpl,
    "sqlite": SQLiteFileSourceImpl,
    "kafka": KafkaSource,
}

_RESOLVER_TYPES = {
    "offline": OfflineResolver,
    "batch": OfflineResolver,
    "online": OnlineResolver,
    "realtime": OnlineResolver,
    "stream": StreamResolver,
    "streaming": StreamResolver,
}


class IncrementalSettings(BaseModel):
    incremental_column: Optional[str]
    lookback_period: Optional[str]
    mode: Literal["row", "group", "parameter"]

    @validator("lookback_period")
    @classmethod
    def validate_lookback_period(cls, value):
        try:
            parse_chalk_duration(value)
        except Exception as e:
            raise ValueError(f"Could not parse value '{value}' as timedelta, {e}")
        return value

    @validator("mode")
    @classmethod
    def validate_mode(cls, mode, values):
        if mode in ["row", "group"] and not values["incremental_column"]:
            raise ValueError(f"'incremental_column' must be set if mode is 'row' or 'group'.")
        return mode


class CommentDict(BaseModel):
    source: str
    resolves: str
    incremental: Optional[IncrementalSettings]
    tags: Optional[List[str]]
    environment: Optional[List[str]]
    count: Optional[Literal[1, "one"]]
    cron: Optional[str]
    machine_type: Optional[str]
    max_staleness: Optional[str]
    message: Optional[str]
    owner: Optional[str]
    type: Optional[str]

    @validator("tags", "environment", pre=True)
    @classmethod
    def validate_list_inputs(cls, value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [value]
        raise ValueError(f"Value {value} must be a string or a list of strings.")

    @validator("cron", "max_staleness")
    @classmethod
    def validate_timedelta(cls, string):
        try:
            parse_chalk_duration(string)
        except Exception as e:
            raise ValueError(f"Could not parse value '{string}' as timedelta, {e}")
        return string

    @validator("type")
    @classmethod
    def validate_type(cls, resolver_type):
        if resolver_type not in _RESOLVER_TYPES:
            raise ValueError(
                f"Resolver type '{resolver_type}' not supported. "
                f"'online', 'offline' and 'streaming' are supported options"
            )
        return resolver_type


@dataclasses.dataclass
class ResolverError:
    """Generic class for returning errors at any point during resolution process"""

    display: str
    path: str
    parameter: Optional[str]


@dataclasses.dataclass
class ResolverResult:
    """Chief return class with resolver we actually use"""

    resolver: Optional[OnlineResolver]
    errors: List[ResolverError]
    db: Optional[TableIngestProtocol]
    fields: Optional[Dict[str, str]]
    args: Optional[Dict[str, str]]


@dataclasses.dataclass
class SQLStringResult:
    """Class for getting the sql string from the file"""

    path: str
    sql_string: Optional[str]
    error: Optional[ResolverError]

    @classmethod
    def fail(cls, display_error: str, path: str) -> "SQLStringResult":
        return cls(path=path, sql_string=None, error=ResolverError(display=display_error, path=path, parameter=None))


@dataclasses.dataclass
class GlotResult:
    """Class for editing the sql string, and using sqlglot on sql string"""

    sql_string: str
    glot: Optional[Expression]
    args: Optional[Dict[str, str]]
    default_args: List[Optional[str]]
    errors: List[ResolverError]


@dataclasses.dataclass
class ParseResult:
    """Class for important info gathered from glot"""

    sql_string: str
    comment_dict: Optional[CommentDict]
    fields: Optional[Dict[str, str]]
    namespace: Optional[str]
    source: Optional[Union[BaseSQLSource, StreamSource]]
    docstring: Optional[str]
    errors: List[ResolverError]


def get_sql_file_resolvers(
    sql_file_resolve_location: Path, sources: Iterable[BaseSQLSource]
) -> Iterable[ResolverResult]:
    """Iterate through all `.chalk.sql` filepaths, gather the sql strings, and get a resolver hopefully for each."""
    for dp, dn, fn in os.walk(os.path.expanduser(sql_file_resolve_location)):
        for f in fn:
            filepath = os.path.join(dp, f)
            if not filepath.endswith(".chalk.sql"):
                continue
            sql_string_result = _get_sql_string(filepath)
            yield get_sql_file_resolver(sources, sql_string_result)


def get_sql_file_resolver(sources: Iterable[BaseSQLSource], sql_string_result: SQLStringResult) -> ResolverResult:
    """Parse the sql strings and get a ResolverResult from each"""
    if sql_string_result.error:
        return ResolverResult(resolver=None, errors=[sql_string_result.error], db=None, fields=None, args=None)
    path = sql_string_result.path

    errors: List[ResolverError] = []
    glot_result: GlotResult = _get_sql_glot(sql_string_result.sql_string, path)
    if glot_result.errors:
        return ResolverResult(resolver=None, errors=glot_result.errors, db=None, fields=None, args=None)

    parsed: ParseResult = _parse_glot(glot_result, path, sources)
    if parsed.errors:
        return ResolverResult(resolver=None, errors=parsed.errors, db=parsed.source, fields=None, args=None)

    # validate inputs and outputs as real features in graph
    inputs: List[Feature] = []
    for arg in glot_result.args.values():
        try:
            inputs.append(Feature.from_root_fqn(arg))
        except Exception as e:
            errors.append(
                ResolverError(display=f"Cannot find input feature '{arg}' in graph, {e}", path=path, parameter=arg)
            )
    outputs: List[Feature] = []
    for output in parsed.fields.values():
        try:
            outputs.append(Feature.from_root_fqn(output))
        except Exception as e:
            errors.append(
                ResolverError(
                    display=f"Cannot find output feature '{output}' in graph, {e}", path=path, parameter=output
                )
            )

    resolver_type_str = parsed.comment_dict.type if parsed.comment_dict.type else "online"
    resolver_type = _RESOLVER_TYPES[resolver_type_str]

    if resolver_type == StreamResolver:
        result: ResolverResult = _get_stream_resolver(path, glot_result, parsed, outputs)
        return result

    result = ResolverResult(resolver=None, errors=errors, db=parsed.source, fields=None, args=None)

    incremental_dict = parsed.comment_dict.incremental.dict() if parsed.comment_dict.incremental else None
    return_one = parsed.comment_dict.count

    # function for online resolver to process
    def fn(
        *input_values,
        database=parsed.source,
        sql_query=parsed.sql_string,
        field_dict=parsed.fields,
        args_dict=glot_result.args,
        incremental=incremental_dict,
    ):
        arg_dict = {arg: input_value for input_value, arg in zip(input_values, args_dict.keys())}
        func = database.query_string(
            query=sql_query,
            fields=field_dict,
            args=arg_dict,
        )
        if incremental:
            func = func.incremental(**incremental)
        if return_one:
            func = func.one()
        return func

    if result.errors:
        return result

    if return_one:
        output = Features[tuple(outputs)]
    else:
        output = DataFrame[tuple(outputs)]

    default_args = [ResolverArgErrorHandler(default_value) for default_value in glot_result.default_args]

    filename = os.path.basename(path)
    # attempt to instantiate the resolver
    try:
        resolver = resolver_type(
            filename=path,
            function_definition=_remove_comments(sql_string_result.sql_string),
            fqn=filename.replace(".chalk.sql", ""),
            doc=parsed.docstring,
            inputs=inputs,
            output=output,
            fn=fn,
            environment=parsed.comment_dict.environment,
            tags=parsed.comment_dict.tags,
            max_staleness=parsed.comment_dict.max_staleness,
            cron=parsed.comment_dict.cron,
            machine_type=parsed.comment_dict.machine_type,
            when=None,
            state=None,
            default_args=default_args,
            owner=parsed.comment_dict.owner,
        )
    except Exception as e:
        result.errors.append(
            ResolverError(
                display=f"{resolver_type_str.capitalize()} resolver could not be instantiated, {e}",
                path=path,
                parameter=None,
            )
        )
        return result

    result.resolver = resolver
    result.fields = parsed.fields
    result.args = glot_result.args
    return result


def _get_sql_string(path: str) -> SQLStringResult:
    """Attempt to get a sql string from a filepath and gracefully exit if unable to"""
    sql_string_result = SQLStringResult(path=path, sql_string=None, error=None)
    if not path.endswith(".chalk.sql"):
        return SQLStringResult.fail(display_error=f"sql resolver file '{path}' must end in '.chalk.sql'", path=path)
    sql_string = None
    if os.path.isfile(path):
        with open(path) as f:
            sql_string = f.read()
    else:
        caller_filename = inspect.stack()[1].filename
        dir_path = os.path.dirname(os.path.realpath(caller_filename))
        if isinstance(path, bytes):
            path = path.decode("utf-8")
        relative_path = os.path.join(dir_path, path)
        if os.path.isfile(relative_path):
            with open(relative_path) as f:
                sql_string = f.read()
    if sql_string is None:
        return SQLStringResult.fail(display_error=f"Cannot find file '{path}'", path=path)
    sql_string_result.sql_string = sql_string
    return sql_string_result


def _get_sql_glot(sql_string: str, path: str) -> GlotResult:
    """Get sqlglot from sql string and gracefully exit if unable to"""
    try:
        import sqlglot
        import sqlglot.expressions
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    glot_result = GlotResult(sql_string=sql_string, glot=None, args=None, default_args=[], errors=[])
    args = {}  # sql string -> input feature string
    variables = set(re.findall("\\${.*?\\}", sql_string))
    # replace ?{variable_name} with :variable_name for sqlalchemy, and keep track of input args necessary
    for variable_pattern in variables:
        has_default_arg = False
        variable = variable_pattern[2:-1]  # cut off ${ and }
        for split_var in ["|", " or "]:  # default argument
            # TODO cannot parse something like {Transaction.category or "Waffles or Pancakes"} yet
            if split_var in variable:
                split = variable.split(split_var)
                if len(split) != 2:
                    glot_result.errors.append(
                        ResolverError(
                            display=f"If character '|' is used, both variable name and default value must be "
                            f'specified in ({variable}) like \'?{{variable_name | "default_value"}}',
                            path=path,
                            parameter=None,
                        )
                    )
                else:  # has default argument
                    variable = split[0].strip()
                    default_arg = split[1].strip()
                    default_arg = json.loads(default_arg)
                    f = Feature.from_root_fqn(variable)
                    default_arg = f.converter.from_json_to_rich(default_arg)
                    glot_result.default_args.append(default_arg)
                    has_default_arg = True
        if not has_default_arg:
            # TODO default value of None should be refactored since None is a legitimate default value
            glot_result.default_args.append(None)
        period_replaced = variable.replace(".", "_")
        sql_safe_str = f"__chalk_{period_replaced}__"
        sql_string = sql_string.replace(variable_pattern, f":{sql_safe_str}")
        args[sql_safe_str] = variable

    glot_result.sql_string = sql_string
    glot_result.args = args
    try:
        glot_result.glot = sqlglot.parse_one(glot_result.sql_string)
    except Exception as e:
        glot_result.errors.append(
            ResolverError(display=f"Cannot SQL parse {glot_result.sql_string}, {e}", path=path, parameter=None)
        )
        return glot_result
    if not isinstance(glot_result.glot, sqlglot.expressions.Select):
        glot_result.errors.append(
            ResolverError(
                display=f"SQL query {glot_result.sql_string} should be of 'SELECT' type", path=path, parameter=None
            )
        )
    return glot_result


def _parse_glot(glot_result: GlotResult, path: str, sources: Iterable[BaseSQLSource]) -> ParseResult:
    """Parse useful info from sqlglot and gracefully exit if unable to"""
    parse_result = ParseResult(
        sql_string=glot_result.sql_string,
        comment_dict=None,
        fields=None,
        namespace=None,
        source=None,
        docstring=None,
        errors=[],
    )

    # parse comments into dictionary
    comments = ""
    docstring = ""
    for comment in glot_result.glot.comments:
        if comment.strip().startswith("-"):
            comments += f"{comment}\n"
        else:
            split = comment.split(":")
            if len(split) != 2:
                docstring += f"{comment.strip()}\n"
            else:
                comments += f"{comment}\n"
    try:
        comment_dict = yaml.safe_load(comments)
    except Exception as e:
        parse_result.errors.append(
            ResolverError(
                display=f"Comments key-values '{comments}' must be of YAML form, {e}",
                path=path,
                parameter=comments,
            )
        )

    if parse_result.errors:
        return parse_result

    try:
        comment_dict_object = CommentDict.parse_obj(comment_dict)
    except ValidationError as e:
        for error in e.errors():
            parse_result.errors.append(
                ResolverError(
                    display=f"Could not parse comment(s) '{'.'.join(error['loc'])}': {error['msg']}",
                    path=path,
                    parameter=comment_dict,
                )
            )
    if parse_result.errors:
        return parse_result

    parse_result.comment_dict = comment_dict_object
    parse_result.docstring = docstring.strip()

    # define a source SQL database. Can either specify name or kind if only one of the kind is present.
    source_name = parse_result.comment_dict.source
    source = None
    if source_name not in _SOURCES:  # actual name of source
        for possible_source in sources:
            if possible_source.name == source_name:
                source = possible_source
    else:
        for possible_source in sources:
            if isinstance(possible_source, _SOURCES.get(source_name)):
                if source:
                    parse_result.errors.append(
                        ResolverError(
                            display=f"More than one {source_name} source exists. Instead, refer to the integration by "
                            f"name among ({[source.name for source in sources]}).",
                            path=path,
                            parameter=source_name,
                        )
                    )
                source = possible_source
    if not source:
        parse_result.errors.append(
            ResolverError(display=f"Source {source_name} not found", path=path, parameter=source_name)
        )
    parse_result.source = source

    if parse_result.errors:
        return parse_result

    # get resolver fields: which columns selected will match to which chalk feature?
    namespace = parse_result.comment_dict.resolves
    # TODO: should handle parsing of 'resolves' list of features instead of namespace in the future
    parse_result.namespace = namespace
    fields = {}  # sql string -> output feature string

    for column_name in glot_result.glot.named_selects:
        fields[column_name] = f"{namespace}.{column_name}"
    parse_result.fields = fields

    return parse_result


def _get_stream_resolver(
    path: str, glot_result: GlotResult, parsed: ParseResult, outputs: List[Feature]
) -> ResolverResult:
    errors = []
    result = ResolverResult(resolver=None, errors=errors, db=parsed.source, fields=None, args=None)

    output_features = Features[DataFrame[tuple(outputs)]]

    if isinstance(output_features.features[0], type) and issubclass(output_features.features[0], DataFrame):
        output_feature_fqns = set(f.fqn for f in cast(Type[DataFrame], output_features.features[0]).columns)
    else:
        output_feature_fqns = set(f.fqn for f in output_features.features)

    signature = StreamResolverSignature(
        params=[],
        output_feature_fqns=output_feature_fqns,
    )

    sql_query: str = _remove_comments(parsed.sql_string)
    filename = os.path.basename(path)

    try:

        def fn():
            return sql_query

        # attempt to instantiate the resolver
        resolver = StreamResolver(
            function_definition=sql_query,
            fqn=filename.replace(".chalk.sql", ""),
            filename=path,
            source=parsed.source,
            fn=fn,
            environment=parsed.comment_dict.environment,
            doc=parsed.docstring,
            module=filename.replace(".chalk.sql", ""),
            mode=None,
            machine_type=parsed.comment_dict.machine_type,
            message=parsed.comment_dict.message,
            output=output_features,
            signature=signature,
            state=None,
            sql_query=sql_query,
            owner=parsed.comment_dict.owner,
        )
    except Exception as e:
        result.errors.append(
            ResolverError(
                display=f"Streaming resolver could not be instantiated, {e}",
                path=path,
                parameter=None,
            )
        )
        return result

    result.resolver = resolver
    result.fields = parsed.fields
    result.args = glot_result.args
    return result


def _remove_comments(sql_string: str) -> str:
    sql_string = re.sub(
        re.compile("/\\*.*?\\*/", re.DOTALL), "", sql_string
    )  # remove all occurrences streamed comments (/*COMMENT */) from string
    sql_string = re.sub(
        re.compile("//.*?\n"), "", sql_string
    )  # remove all occurrence single-line comments (//COMMENT\n ) from string
    sql_string = re.sub(
        re.compile("--.*?\n"), "", sql_string
    )  # remove all occurrence single-line comments (//COMMENT\n ) from string
    return sql_string.strip()
