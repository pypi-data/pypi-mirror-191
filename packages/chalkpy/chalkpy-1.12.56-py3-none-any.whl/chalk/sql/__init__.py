from os import PathLike
from typing import Optional, Union, overload

from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.integrations.bigquery import BigQuerySourceImpl
from chalk.sql._internal.integrations.cloudsql import CloudSQLSourceImpl
from chalk.sql._internal.integrations.mysql import MySQLSourceImpl
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.sql._internal.integrations.redshift import RedshiftSourceImpl
from chalk.sql._internal.integrations.snowflake import SnowflakeSourceImpl
from chalk.sql._internal.integrations.sqlite import SQLiteFileSourceImpl, SQLiteInMemorySourceImpl
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import (
    BaseSQLSourceProtocol,
    ChalkQueryProtocol,
    SQLSourceWithTableIngestProtocol,
    StringChalkQueryProtocol,
    TableIngestProtocol,
)


@overload
def SnowflakeSource() -> BaseSQLSourceProtocol:
    """Connect to the only configured Snowflake database.

    If you have only one Snowflake connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SnowflakeSource()
    """


@overload
def SnowflakeSource(*, name: str) -> BaseSQLSourceProtocol:
    """Chalk's injects environment variables to support data integrations.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SnowflakeSource(name="RISK")
    """
    ...


@overload
def SnowflakeSource(
    *,
    account_identifier: str = ...,
    warehouse: str = ...,
    user: str = ...,
    password: str = ...,
    db: str = ...,
    schema: str = ...,
    role: str = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    account_identifier
        Your Snowflake account identifier.
    warehouse
        Snowflake warehouse to use.
    user
        Username to connect to Snowflake.
    password
        The password to use.
    db
        Database to use.
    schema
        Snowflake schema in the database to use.
    role
        Snowflake role name to use.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> snowflake = SnowflakeSource(
    ...     db=os.getenv("SNOWSQL_DATABASE"),
    ...     schema=os.getenv("SNOWSQL_SCHEMA"),
    ...     role=os.getenv("SNOWSQL_ROLE"),
    ...     warehouse=os.getenv("SNOWSQL_WAREHOUSE"),
    ...     user=os.getenv("SNOWSQL_USER"),
    ...     password=os.getenv("SNOWSQL_PWD"),
    ...     account_identifier=os.getenv("SNOWSQL_ACCOUNT_IDENTIFIER")
    ... )
    """
    ...


def SnowflakeSource(
    *,
    name: Optional[str] = None,
    account_identifier: Optional[str] = None,
    warehouse: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    db: Optional[str] = None,
    schema: Optional[str] = None,
    role: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return SnowflakeSourceImpl(
        name=name,
        account_identifier=account_identifier,
        warehouse=warehouse,
        user=user,
        password=password,
        db=db,
        schema=schema,
        role=role,
    )


@overload
def PostgreSQLSource() -> SQLSourceWithTableIngestProtocol:
    """Connect to the only configured PostgreSQL database.

    If you have only one PostgreSQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> pg = PostgreSQLSource()
    """
    ...


@overload
def PostgreSQLSource(
    *,
    host: str = ...,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
) -> SQLSourceWithTableIngestProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    host
        Name of host to connect to.
    port
        The port number to connect to at the server host.
    db
        The database name.
    user
        PostgreSQL username to connect as.
    password
        The password to be used if the server demands password authentication.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> pg = PostgreSQLSource(
    ...     host=os.getenv("PGHOST"),
    ...     port=os.getenv("PGPORT"),
    ...     db=os.getenv("PGDATABASE"),
    ...     user=os.getenv("PGUSER"),
    ...     password=os.getenv("PGPASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return pg.query_string("select name from users where id = 4").one()
    """
    ...


@overload
def PostgreSQLSource(*, name: str) -> SQLSourceWithTableIngestProtocol:
    """If you have only one PostgreSQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = PostgreSQLSource(name="RISK")
    """
    ...


def PostgreSQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
) -> TableIngestProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    host
        Name of host to connect to.
    port
        The port number to connect to at the server host.
    db
        The database name.
    user
        PostgreSQL username to connect as.
    password
        The password to be used if the server demands password authentication.
    name
        The name of the integration, as configured in your dashboard.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.
    """
    return PostgreSQLSourceImpl(host, port, db, user, password, name)


@overload
def MySQLSource(
    *,
    host: str = ...,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
) -> SQLSourceWithTableIngestProtocol:
    """

    Parameters
    ----------
    host
    port
    db
    user
    password

    Returns
    -------

    """
    ...


@overload
def MySQLSource() -> SQLSourceWithTableIngestProtocol:
    """If you have only one MySQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> mysql = MySQLSource()
    """
    ...


@overload
def MySQLSource(*, name: str) -> SQLSourceWithTableIngestProtocol:
    """If you have only one MySQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = MySQLSource(name="RISK")
    """
    ...


def MySQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
) -> SQLSourceWithTableIngestProtocol:
    return MySQLSourceImpl(host, port, db, user, password, name)


def SQLiteInMemorySource(name: Optional[str] = None) -> SQLSourceWithTableIngestProtocol:
    """Testing SQL source.

    If you have only one SQLiteInMemorySource integration, there's no need to provide
    a distinguishing name.

    Parameters
    ----------
    name
        The name of the integration.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = MySQLSource(name="RISK")
    """
    return SQLiteInMemorySourceImpl(name)


def SQLiteFileSource(filename: Union[str, PathLike], name: Optional[str] = None) -> SQLSourceWithTableIngestProtocol:
    return SQLiteFileSourceImpl(filename, name)


@overload
def RedshiftSource(
    *,
    host: str = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    host
        Name of host to connect to.
    db
        The database name.
    user
        Redshify username to connect as.
    password
        The password for the Redshift database.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> redshift = RedshiftSource(
    ...     host=os.getenv("REDSHIFT_HOST"),
    ...     db=os.getenv("REDSHIFT_DB"),
    ...     user=os.getenv("REDSHIFT_USER"),
    ...     password=os.getenv("REDSHIFT_PASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return redshift.query_string("select name from users where id = 4").one()
    """
    ...


@overload
def RedshiftSource(*, name: str) -> BaseSQLSourceProtocol:
    """If you have only one Redshift integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = RedshiftSource(name="RISK")
    """
    ...


@overload
def RedshiftSource() -> BaseSQLSourceProtocol:
    """If you have only one Redshift connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = RedshiftSource()
    """
    ...


def RedshiftSource(
    *,
    host: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return RedshiftSourceImpl(host, db, user, password, name)


@overload
def BigQuerySource() -> BaseSQLSourceProtocol:
    """If you have only one BigQuery connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = BigQuerySource()
    """
    ...


@overload
def BigQuerySource(*, name: str) -> BaseSQLSourceProtocol:
    """If you have only one BigQuery integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = BigQuerySource(name="RISK")
    """
    ...


def BigQuerySource(
    *,
    name: Optional[str] = None,
    project: Optional[str] = None,
    dataset: Optional[str] = None,
    location: Optional[str] = None,
    credentials_base64: Optional[str] = None,
    credentials_path: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return BigQuerySourceImpl(
        name=name,
        project=project,
        dataset=dataset,
        location=location,
        credentials_base64=credentials_base64,
        credentials_path=credentials_path,
    )


@overload
def CloudSQLSource() -> BaseSQLSourceProtocol:
    """If you have only one CloudSQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = CloudSQLSource()
    """
    ...


@overload
def CloudSQLSource(*, name: str) -> BaseSQLSourceProtocol:
    """If you have only one CloudSQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = CloudSQLSource(name="RISK")
    """
    ...


@overload
def CloudSQLSource(
    *,
    instance_name: str = None,
    db: str = None,
    user: str = None,
    password: str = None,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    instance_name
        The name of the Cloud SQL instance, as defined in your GCP console.
    db
        Database to use.
    user
        Username to use.
    password
        The password to use.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> CloudSQLSource(
    ...     instance_name=os.getenv("CLOUDSQL_INSTANCE_NAME"),
    ...     db=os.getenv("CLOUDSQL_DB"),
    ...     user=os.getenv("CLOUDSQL_USER"),
    ...     password=os.getenv("CLOUDSQL_PASSWORD"),
    ... )
    """


def CloudSQLSource(
    *,
    name: Optional[str] = None,
    instance_name: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
) -> BaseSQLSourceProtocol:
    return CloudSQLSourceImpl(
        name=name,
        instance_name=instance_name,
        db=db,
        user=user,
        password=password,
    )


__all__ = [
    "BaseSQLSourceProtocol",
    "BigQuerySource",
    "CloudSQLSource",
    "MySQLSource",
    "PostgreSQLSource",
    "RedshiftSource",
    "SQLiteFileSource",
    "SQLiteInMemorySource",
    "SnowflakeSource",
    "FinalizedChalkQuery",
    "ChalkQueryProtocol",
    "StringChalkQueryProtocol",
    "TableIngestProtocol",
    "SQLSourceWithTableIngestProtocol",
    "IncrementalSettings",
]
