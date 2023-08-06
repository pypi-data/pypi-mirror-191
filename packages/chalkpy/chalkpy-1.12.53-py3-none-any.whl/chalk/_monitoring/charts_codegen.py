# AUTO-GENERATED FILE. Do not edit.
from typing import Any, Dict, List, Literal, Optional, Tuple, TypeVar, Union

from chalk._monitoring.charts_enums_codegen import GroupByKind
from chalk._monitoring.charts_series_base import ResolverType, SeriesBase
from chalk.features.resolver import ResolverProtocol


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
