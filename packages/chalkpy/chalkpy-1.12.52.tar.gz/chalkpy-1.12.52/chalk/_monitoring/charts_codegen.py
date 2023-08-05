# AUTO-GENERATED FILE. Do not edit.
import dataclasses
import zlib
from copy import deepcopy
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Tuple, TypeVar, Union

from chalk.features import FeatureWrapper
from chalk.features.resolver import Resolver, ResolverProtocol


class MetricKind(str, Enum):
    FEATURE_REQUEST_COUNT = "FEATURE_REQUEST_COUNT"
    FEATURE_LATENCY = "FEATURE_LATENCY"
    FEATURE_STALENESS = "FEATURE_STALENESS"
    FEATURE_VALUE = "FEATURE_VALUE"
    FEATURE_WRITE = "FEATURE_WRITE"
    FEATURE_NULL_RATIO = "FEATURE_NULL_RATIO"

    RESOLVER_REQUEST_COUNT = "RESOLVER_REQUEST_COUNT"
    RESOLVER_LATENCY = "RESOLVER_LATENCY"
    RESOLVER_SUCCESS_RATIO = "RESOLVER_SUCCESS_RATIO"

    QUERY_COUNT = "QUERY_COUNT"
    QUERY_LATENCY = "QUERY_LATENCY"
    QUERY_SUCCESS_RATIO = "QUERY_SUCCESS_RATIO"

    BILLING_INFERENCE = "BILLING_INFERENCE"
    BILLING_CRON = "BILLING_CRON"
    BILLING_MIGRATION = "BILLING_MIGRATION"

    CRON_COUNT = "CRON_COUNT"
    CRON_LATENCY = "CRON_LATENCY"

    STREAM_MESSAGES_PROCESSED = "STREAM_MESSAGES_PROCESSED"
    STREAM_MESSAGE_LATENCY = "STREAM_MESSAGE_LATENCY"

    STREAM_WINDOWS_PROCESSED = "STREAM_WINDOWS_PROCESSED"
    STREAM_WINDOW_LATENCY = "STREAM_WINDOW_LATENCY"


class FilterKind(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    FEATURE_TAG = "FEATURE_TAG"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"
    RESOLVER_TAG = "RESOLVER_TAG"

    CRON_STATUS = "CRON_STATUS"
    MIGRATION_STATUS = "MIGRATION_STATUS"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"
    OPERATION_ID = "OPERATION_ID"

    QUERY_NAME = "QUERY_NAME"
    QUERY_STATUS = "QUERY_STATUS"

    IS_NULL = "IS_NULL"


ResolverType = Literal["online", "offline", "stream"]
ResolverNameType = Union[Resolver, str]


class ComparatorKind(str, Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    ONE_OF = "ONE_OF"


class WindowFunctionKind(str, Enum):
    COUNT = "COUNT"
    MEAN = "MEAN"
    SUM = "SUM"
    MIN = "MIN"
    MAX = "MAX"

    PERCENTILE_99 = "PERCENTILE_99"
    PERCENTILE_95 = "PERCENTILE_95"
    PERCENTILE_75 = "PERCENTILE_75"
    PERCENTILE_50 = "PERCENTILE_50"
    PERCENTILE_25 = "PERCENTILE_25"
    PERCENTILE_5 = "PERCENTILE_5"

    ALL_PERCENTILES = "ALL_PERCENTILES"

    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__


class GroupByKind(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    IS_NULL = "IS_NULL"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"

    QUERY_STATUS = "QUERY_STATUS"
    QUERY_NAME = "QUERY_NAME"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"


class ChartLinkKind(str, Enum):
    resolver = "resolver"
    feature = "feature"
    query = "query"
    manual = "manual"


@dataclasses.dataclass
class MetricFilter:
    kind: FilterKind
    comparator: ComparatorKind
    value: List[str]


@dataclasses.dataclass
class ThresholdFunction:
    lhs: "SeriesBase"
    operation: str
    rhs: float


window_function_args: Dict[WindowFunctionKind, str] = {
    WindowFunctionKind.COUNT: "count",
    WindowFunctionKind.MEAN: "mean",
    WindowFunctionKind.SUM: "sum",
    WindowFunctionKind.MIN: "min",
    WindowFunctionKind.MAX: "max",
    WindowFunctionKind.PERCENTILE_99: "99%",
    WindowFunctionKind.PERCENTILE_95: "95%",
    WindowFunctionKind.PERCENTILE_75: "75%",
    WindowFunctionKind.PERCENTILE_50: "50%",
    WindowFunctionKind.PERCENTILE_25: "25%",
    WindowFunctionKind.PERCENTILE_5: "5%",
    WindowFunctionKind.ALL_PERCENTILES: "all",
}
TSeries = TypeVar("TSeries", bound="SeriesBase")


class SeriesBase:
    def __init__(
        self,
        name: str,
        metric: Union[MetricKind, str],
        window_function: Optional[Union[WindowFunctionKind, str]] = None,
        time_shift: Optional[int] = None,
    ):
        self._name = name
        self._metric = MetricKind(metric.upper()) if metric else None
        self._filters: List[MetricFilter] = []
        if window_function:
            if WindowFunctionKind.has_member_key(window_function.upper()):
                window_function_kind = WindowFunctionKind(window_function.upper())
            else:
                window_function_kind = self._get_window_function_type(window_function.upper())
                if not window_function_kind:
                    raise ValueError(f"'window_function' value '{window_function}' 'invalid for WindowFunctionKind")
        else:
            window_function_kind = None
        self._window_function = window_function_kind
        self._group_by: List[GroupByKind] = []
        self._time_shift = time_shift
        self._entity_kind = ChartLinkKind.manual
        self._entity_id = None

    @staticmethod
    def _get_window_function_type(key: str) -> Union[WindowFunctionKind, None]:
        window_function_value_dict = {
            "99%": WindowFunctionKind.PERCENTILE_99,
            "95%": WindowFunctionKind.PERCENTILE_95,
            "75%": WindowFunctionKind.PERCENTILE_75,
            "50%": WindowFunctionKind.PERCENTILE_50,
            "25%": WindowFunctionKind.PERCENTILE_25,
            "5%": WindowFunctionKind.PERCENTILE_5,
            "99": WindowFunctionKind.PERCENTILE_99,
            "95": WindowFunctionKind.PERCENTILE_95,
            "75": WindowFunctionKind.PERCENTILE_75,
            "50": WindowFunctionKind.PERCENTILE_50,
            "25": WindowFunctionKind.PERCENTILE_25,
            "5": WindowFunctionKind.PERCENTILE_5,
            "ALL": WindowFunctionKind.ALL_PERCENTILES,
        }
        return window_function_value_dict.get(key)

    def _where(
        self: TSeries,
        feature: Optional[Union[List[Any], Any]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
        cron_status: Optional[Literal["success", "failure"]] = None,
        migration_status: Optional[Literal["success", "failure"]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        cache_hit: Optional[bool] = None,
        is_null: Optional[bool] = None,
        equals: Optional[bool] = True,
    ) -> TSeries:
        copy = self._copy_with()
        success_dict = {"success": True, "failure": False}
        if feature:
            feature_name = [feature] if not isinstance(feature, list) else feature
            copy = copy._feature_name_filter(*feature_name, equals=equals)
        if resolver:
            resolver_name = [resolver] if not isinstance(resolver, list) else resolver
            copy = copy._resolver_name_filter(*resolver_name, equals=equals)
        if feature_tag:
            feature_tag = [feature_tag] if isinstance(feature_tag, str) else feature_tag
            copy = copy._string_filter(*feature_tag, kind=FilterKind.FEATURE_TAG, equals=equals)
        if resolver_tag:
            resolver_tag = [resolver_tag] if isinstance(resolver_tag, str) else resolver_tag
            copy = copy._string_filter(*resolver_tag, kind=FilterKind.RESOLVER_TAG, equals=equals)
        if operation_id:
            operation_id = [operation_id] if isinstance(operation_id, str) else operation_id
            copy = copy._string_filter(*operation_id, kind=FilterKind.OPERATION_ID, equals=equals)
        if query_name:
            query_name = [query_name] if isinstance(query_name, str) else query_name
            copy = copy._string_filter(*query_name, kind=FilterKind.QUERY_NAME, equals=equals)
        if feature_status:
            copy = copy._status_filter(kind=FilterKind.FEATURE_STATUS, success=success_dict[feature_status] == equals)
        if resolver_status:
            copy = copy._status_filter(kind=FilterKind.RESOLVER_STATUS, success=success_dict[resolver_status] == equals)
        if cron_status:
            copy = copy._status_filter(kind=FilterKind.CRON_STATUS, success=success_dict[cron_status] == equals)
        if migration_status:
            copy = copy._status_filter(
                kind=FilterKind.MIGRATION_STATUS, success=success_dict[migration_status] == equals
            )
        if query_status:
            copy = copy._status_filter(kind=FilterKind.QUERY_STATUS, success=success_dict[query_status] == equals)
        if resolver_type:
            resolver_type = [resolver_type] if not isinstance(resolver_type, list) else resolver_type
            copy = copy.with_resolver_type_filter(*resolver_type, equals=equals)
        if cache_hit is not None:
            copy = copy._true_false_filter(kind=FilterKind.CACHE_HIT, value=cache_hit == equals)
        if is_null is not None:
            copy = copy._true_false_filter(kind=FilterKind.IS_NULL, value=is_null == equals)
        return copy

    def _feature_name_filter(self: TSeries, *features: Tuple[Any], equals: bool) -> TSeries:
        if not features:
            raise ValueError(f"One or more Chalk Features must be supplied.")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(features) == 1 or not equals:
            for feature in features:
                value = str(feature) if isinstance(feature, FeatureWrapper) else feature
                metric_filter = MetricFilter(kind=FilterKind.FEATURE_NAME, comparator=comparator, value=[value])
                copy._filters.append(metric_filter)
            if len(features) == 1:
                feature = features[0]
                copy._entity_id = str(feature) if isinstance(feature, FeatureWrapper) else feature
                copy._entity_kind = ChartLinkKind.feature
        else:
            value = [str(feature) if isinstance(feature, FeatureWrapper) else feature for feature in features]
            metric_filter = MetricFilter(kind=FilterKind.FEATURE_NAME, comparator=ComparatorKind.ONE_OF, value=value)
            copy._filters.append(metric_filter)
        return copy

    def _resolver_name_filter(
        self: TSeries, *resolvers: Tuple[Union[ResolverNameType, ResolverProtocol]], equals: bool
    ) -> TSeries:
        if not resolvers:
            raise ValueError(f"One or more Chalk Resolvers must be supplied.")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(resolvers) == 1 or not equals:
            for resolver in resolvers:
                value = resolver.fqn if isinstance(resolver, Resolver) else resolver
                metric_filter = MetricFilter(kind=FilterKind.RESOLVER_NAME, comparator=comparator, value=[value])
                copy._filters.append(metric_filter)
            if len(resolvers) == 1:
                resolver = resolvers[0]
                copy._entity_id = resolver.fqn if isinstance(resolver, Resolver) else resolver
                copy._entity_kind = ChartLinkKind.resolver
        else:
            value = [resolver.fqn if isinstance(resolver, Resolver) else resolver for resolver in resolvers]
            metric_filter = MetricFilter(kind=FilterKind.RESOLVER_NAME, comparator=ComparatorKind.ONE_OF, value=value)
            copy._filters.append(metric_filter)
        return copy

    def _string_filter(self: TSeries, *strings: Tuple[str], kind: FilterKind, equals=True) -> TSeries:
        if not strings:
            raise ValueError(f"One or more arguments must be supplied for this filter")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(strings) == 1 or not equals:
            for string in strings:
                metric_filter = MetricFilter(kind=kind, comparator=comparator, value=[string])
                copy._filters.append(metric_filter)
            if len(strings) == 1 and kind == FilterKind.QUERY_NAME:
                copy._entity_id = strings[0]
                copy._entity_kind = ChartLinkKind.query
        else:
            metric_filter = MetricFilter(kind=kind, comparator=ComparatorKind.ONE_OF, value=list(strings))
            copy._filters.append(metric_filter)
        return copy

    def with_resolver_type_filter(
        self: TSeries, *resolver_types: Tuple[Literal["online", "offline", "stream"]], equals=True
    ) -> TSeries:
        if not resolver_types:
            raise ValueError(f"One or more resolver types from 'online', 'offline', or 'stream' must be supplied")
        if not set(resolver_types).issubset(["online", "offline", "stream"]):
            raise ValueError(f"Resolver types '{resolver_types}' must be one of 'online', 'offline', or 'stream'")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(resolver_types) == 1 or not equals:
            for resolver_type in resolver_types:
                metric_filter = MetricFilter(
                    kind=FilterKind.ONLINE_OFFLINE, comparator=comparator, value=[resolver_type]
                )
                copy._filters.append(metric_filter)
        else:
            metric_filter = MetricFilter(
                kind=FilterKind.ONLINE_OFFLINE, comparator=ComparatorKind.ONE_OF, value=list(resolver_types)
            )
            copy._filters.append(metric_filter)
        return copy

    def _true_false_filter(self: TSeries, kind: FilterKind, value: bool) -> TSeries:
        copy = self._copy_with()
        value = "true" if value else "false"
        metric_filter = MetricFilter(kind=kind, comparator=ComparatorKind.EQ, value=[value])
        copy._filters.append(metric_filter)
        return copy

    def _status_filter(self: TSeries, kind: FilterKind, success: bool) -> TSeries:
        copy = self._copy_with()
        value = "success" if success else "failure"
        metric_filter = MetricFilter(kind=kind, comparator=ComparatorKind.EQ, value=[value])
        copy._filters.append(metric_filter)
        return copy

    def with_filter(
        self: TSeries,
        kind: Union[FilterKind, str],
        comparator: Union[ComparatorKind, str],
        value: Union[List[str], str],
    ) -> TSeries:
        copy = self._copy_with()
        kind = FilterKind(kind.upper())
        comparator = ComparatorKind(comparator.upper())
        value = [value] if isinstance(value, str) else value
        metric_filter = MetricFilter(kind=kind, comparator=comparator, value=value)
        copy._filters.append(metric_filter)
        return copy

    def with_window_function(self: TSeries, window_function: Union[WindowFunctionKind, str]) -> TSeries:
        copy = self._copy_with()
        copy._window_function = WindowFunctionKind(window_function.upper())
        return copy

    def with_group_by(self: TSeries, group_by: Union[GroupByKind, str]) -> TSeries:
        copy = self._copy_with()
        group_by = GroupByKind(group_by.upper())
        copy._group_by.append(group_by)
        return copy

    def with_time_shift(self: TSeries, time_shift: int) -> TSeries:
        copy = self._copy_with()
        copy._time_shift = time_shift
        return copy

    def _copy_with(self: TSeries) -> TSeries:
        self_copy = deepcopy(self)
        return self_copy

    def __gt__(self, other) -> ThresholdFunction:
        return ThresholdFunction(self, ">", other)

    def __lt__(self, other) -> ThresholdFunction:
        return ThresholdFunction(self, "<", other)

    def __str__(self) -> str:
        return f"Series(name='{self._name}')"

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        metric = str(self._metric) if self._metric else "."
        filter_strings = (
            sorted([f"{f.kind}.{f.comparator}.{'.'.join(f.value)}" for f in self._filters]) if self._filters else "."
        )
        window_function = str(self._window_function) if self._window_function else "."
        group_by = sorted([str(group_by) for group_by in self._group_by]) if self._group_by else "."
        time_shift = str(self._time_shift) if self._time_shift else "."

        series_string = (
            f"series.{name}.{metric}.{'.'.join(filter_strings)}.{window_function}.{'.'.join(group_by)}.{time_shift}"
        )

        return zlib.crc32(series_string.encode())


class Series(SeriesBase):
    def __new__(cls, *args, **kwargs):
        raise ValueError("Please construct a Series with a metric classmethod")

    @classmethod
    def feature_request_count_metric(cls, name: str) -> "_FeatureRequestCountSeries":
        return _FeatureRequestCountSeries(name=name, metric="FEATURE_REQUEST_COUNT", window_function="COUNT")

    @classmethod
    def feature_staleness_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_FeatureStalenessSeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _FeatureStalenessSeries(name=name, metric="FEATURE_STALENESS", window_function=window_function)

    @classmethod
    def feature_value_metric(
        cls,
        name: str,
        window_function: Literal["mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_FeatureValueSeries":
        if window_function not in {"mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"}:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _FeatureValueSeries(name=name, metric="FEATURE_VALUE", window_function=window_function)

    @classmethod
    def feature_null_ratio_metric(cls, name: str) -> "_FeatureNullRatioSeries":
        return _FeatureNullRatioSeries(
            name=name,
            metric="FEATURE_NULL_RATIO",
        )

    @classmethod
    def resolver_request_count_metric(cls, name: str) -> "_ResolverRequestCountSeries":
        return _ResolverRequestCountSeries(name=name, metric="RESOLVER_REQUEST_COUNT", window_function="COUNT")

    @classmethod
    def resolver_latency_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_ResolverLatencySeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _ResolverLatencySeries(name=name, metric="RESOLVER_LATENCY", window_function=window_function)

    @classmethod
    def resolver_success_ratio_metric(cls, name: str) -> "_ResolverSuccessRatioSeries":
        return _ResolverSuccessRatioSeries(
            name=name,
            metric="RESOLVER_SUCCESS_RATIO",
        )

    @classmethod
    def query_count_metric(cls, name: str) -> "_QueryCountSeries":
        return _QueryCountSeries(name=name, metric="QUERY_COUNT", window_function="COUNT")

    @classmethod
    def query_latency_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_QueryLatencySeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _QueryLatencySeries(name=name, metric="QUERY_LATENCY", window_function=window_function)

    @classmethod
    def query_success_ratio_metric(cls, name: str) -> "_QuerySuccessRatioSeries":
        return _QuerySuccessRatioSeries(
            name=name,
            metric="QUERY_SUCCESS_RATIO",
        )

    @classmethod
    def cron_count_metric(cls, name: str) -> "_CronCountSeries":
        return _CronCountSeries(name=name, metric="CRON_COUNT", window_function="COUNT")

    @classmethod
    def cron_latency_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_CronLatencySeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _CronLatencySeries(name=name, metric="CRON_LATENCY", window_function=window_function)

    @classmethod
    def stream_message_latency_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_StreamMessageLatencySeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _StreamMessageLatencySeries(name=name, metric="STREAM_MESSAGE_LATENCY", window_function=window_function)

    @classmethod
    def stream_messages_processed_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_StreamMessagesProcessedSeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _StreamMessagesProcessedSeries(
            name=name, metric="STREAM_MESSAGES_PROCESSED", window_function=window_function
        )

    @classmethod
    def stream_windows_processed_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_StreamWindowsProcessedSeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _StreamWindowsProcessedSeries(
            name=name, metric="STREAM_WINDOWS_PROCESSED", window_function=window_function
        )

    @classmethod
    def stream_window_latency_metric(
        cls,
        name: str,
        window_function: Literal["count", "mean", "sum", "max", "99%", "95%", "75%", "50%", "25%", "5%", "min", "all"],
    ) -> "_StreamWindowLatencySeries":
        if window_function not in {
            "count",
            "mean",
            "sum",
            "max",
            "99%",
            "95%",
            "75%",
            "50%",
            "25%",
            "5%",
            "min",
            "all",
        }:
            raise ValueError(f"window_function value '{window_function}' is not valid")
        return _StreamWindowLatencySeries(name=name, metric="STREAM_WINDOW_LATENCY", window_function=window_function)


class _FeatureRequestCountSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        cache_hit: Optional[bool] = None,
    ) -> "_FeatureRequestCountSeries":
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            cache_hit=cache_hit,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        is_null: Optional[bool] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        cache_hit: Optional[bool] = None,
    ) -> "_FeatureRequestCountSeries":
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            is_null=is_null,
            feature_status=feature_status,
            cache_hit=cache_hit,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_FeatureRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_FeatureRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_is_null(self) -> "_FeatureRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.IS_NULL)
        return copy

    def group_by_feature(self) -> "_FeatureRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class _FeatureStalenessSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
    ) -> "_FeatureStalenessSeries":
        return self._where(
            resolver_type=resolver_type,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
    ) -> "_FeatureStalenessSeries":
        return self._where(
            resolver_type=resolver_type,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_FeatureStalenessSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_FeatureStalenessSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy


class _FeatureValueSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        cache_hit: Optional[bool] = None,
    ) -> "_FeatureValueSeries":
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            cache_hit=cache_hit,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        cache_hit: Optional[bool] = None,
    ) -> "_FeatureValueSeries":
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            cache_hit=cache_hit,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_FeatureValueSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_FeatureValueSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_feature(self) -> "_FeatureValueSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class _FeatureNullRatioSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        cache_hit: Optional[bool] = None,
    ) -> "_FeatureNullRatioSeries":
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            cache_hit=cache_hit,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        feature: Optional[Union[List[Any], Any]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        cache_hit: Optional[bool] = None,
    ) -> "_FeatureNullRatioSeries":
        return self._where(
            resolver_type=resolver_type,
            feature_tag=feature_tag,
            feature=feature,
            feature_status=feature_status,
            cache_hit=cache_hit,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_FeatureNullRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_FeatureNullRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_feature(self) -> "_FeatureNullRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy


class _ResolverRequestCountSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_ResolverRequestCountSeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_ResolverRequestCountSeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_ResolverRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_ResolverRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_resolver(self) -> "_ResolverRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy

    def group_by_resolver_status(self) -> "_ResolverRequestCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy


class _ResolverLatencySeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_ResolverLatencySeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_ResolverLatencySeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_ResolverLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_ResolverLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_resolver(self) -> "_ResolverLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy

    def group_by_resolver_status(self) -> "_ResolverLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy


class _ResolverSuccessRatioSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_ResolverSuccessRatioSeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_ResolverSuccessRatioSeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_ResolverSuccessRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_ResolverSuccessRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def group_by_resolver(self) -> "_ResolverSuccessRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy

    def group_by_resolver_status(self) -> "_ResolverSuccessRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy


class _QueryCountSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_QueryCountSeries":
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_QueryCountSeries":
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            equals=False,
        )

    def group_by_query_status(self) -> "_QueryCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def group_by_query_name(self) -> "_QueryCountSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy


class _QueryLatencySeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_QueryLatencySeries":
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_QueryLatencySeries":
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            query_status=query_status,
            equals=False,
        )

    def group_by_query_status(self) -> "_QueryLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def group_by_query_name(self) -> "_QueryLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy


class _QuerySuccessRatioSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
    ) -> "_QuerySuccessRatioSeries":
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        query_name: Optional[Union[List[str], str]] = None,
    ) -> "_QuerySuccessRatioSeries":
        return self._where(
            resolver_type=resolver_type,
            query_name=query_name,
            equals=False,
        )

    def group_by_query_name(self) -> "_QuerySuccessRatioSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy


class _CronCountSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_CronCountSeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_CronCountSeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )


class _CronLatencySeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_CronLatencySeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_CronLatencySeries":
        return self._where(
            resolver_type=resolver_type,
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_type(self) -> "_CronLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def group_by_cache_hit(self) -> "_CronLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy


class _StreamMessageLatencySeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamMessageLatencySeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamMessageLatencySeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "_StreamMessageLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy


class _StreamMessagesProcessedSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamMessagesProcessedSeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamMessagesProcessedSeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "_StreamMessagesProcessedSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy


class _StreamWindowsProcessedSeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamWindowsProcessedSeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamWindowsProcessedSeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "_StreamWindowsProcessedSeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy


class _StreamWindowLatencySeries(SeriesBase):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def where(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamWindowLatencySeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=True,
        )

    def where_not(
        self,
        resolver_tag: Optional[Union[List[str], str]] = None,
        resolver: Optional[Union[List[Union[ResolverProtocol, str]], Union[ResolverProtocol, str]]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
    ) -> "_StreamWindowLatencySeries":
        return self._where(
            resolver_tag=resolver_tag,
            resolver=resolver,
            resolver_status=resolver_status,
            equals=False,
        )

    def group_by_resolver_status(self) -> "_StreamWindowLatencySeries":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy
