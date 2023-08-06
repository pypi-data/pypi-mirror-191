from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Protocol, Sequence, Union

import pandas as pd

from chalk.client.models import (
    ChalkError,
    FeatureResult,
    OfflineQueryContext,
    OnlineQueryContext,
    ResolverRunResponse,
    WhoAmIResponse,
)
from chalk.features import DataFrame, Feature

if TYPE_CHECKING:
    import polars as pl


class OnlineQueryResponseProtocol(Protocol):
    data: List[FeatureResult]
    """The output features and any query metadata."""

    errors: Optional[List[ChalkError]]
    """Errors encountered while running the resolvers.

    If no errors were encountered, this field is empty.
    """

    def get_feature(self, feature: Union[str, Any]) -> Optional[FeatureResult]:
        """Convenience method for accessing feature result from the data response

        Parameters
        ----------
        feature
            The feature or its string representation.

        Returns
        -------
        FeatureResult | None
            The `FeatureResult` for the feature, if it exists.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> data = ChalkClient().query(...)
        >>> data.get_feature(User.name).ts
        datetime.datetime(2023, 2, 5, 23, 25, 26, 427605)
        >>> data.get_feature("user.name").meta.cache_hit
        False
        """
        ...

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        """Convenience method for accessing feature values from the data response

        Parameters
        ----------
        feature
            The feature or its string representation.

        Returns
        -------
        Any
            The value of the feature.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> data = ChalkClient().query(...)
        >>> data.get_feature_value(User.name)
        "Katherine Johnson"
        >>> data.get_feature_value("user.name")
        "Katherine Johnson"
        """
        ...


class ChalkAPIClientProtocol(Protocol):
    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        context: Optional[OfflineQueryContext] = None,
    ) -> ResolverRunResponse:
        """Triggers a resolver to run.
        See https://docs.chalk.ai/docs/runs for more information.

        Parameters
        ----------
        resolver_fqn
            The fully qualified name of the resolver to trigger.
        context
            The environment under which you'd like to query your data.

        Returns
        -------
        ResolverRunResponse
            Status of the resolver run and the run ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().trigger_resolver_run(
        ...     resolver_fqn="mymodule.fn"
        ... )
        """
        ...

    def get_run_status(self, run_id: str) -> ResolverRunResponse:
        """Retrieves the status of a resolver run.
        See https://docs.chalk.ai/docs/runs for more information.

        Parameters
        ----------
        run_id
            ID of the resolver run to check.

        Returns
        -------
        ResolverRunResponse
            Status of the resolver run and the run ID.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().get_run_status(
        ...     run_id="3",
        ... )
        ResolverRunResponse(
            id="3",
            status=ResolverRunStatus.SUCCEEDED
        )
        """
        ...

    def whoami(self) -> WhoAmIResponse:
        """Checks the identity of your client.

        Useful as a sanity test of your configuration.

        Returns
        -------
        WhoAmIResponse
            The identity of your client

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().whoami()
        WhoAmIResponse(user="44")
        """
        ...

    def query(
        self,
        input: Mapping[Union[str, Feature, Any], Any],
        output: Sequence[Union[str, Feature, Any]],
        staleness: Optional[Mapping[Union[str, Feature, Any], str]] = None,
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> OnlineQueryResponseProtocol:
        """Compute features values using online resolvers.
        See https://docs.chalk.ai/docs/query-basics for more information.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
        output
            Outputs are the features that you'd like to compute from the inputs.
        staleness
            Maximum staleness overrides for any output features or intermediate features.
            See https://docs.chalk.ai/docs/query-caching for more information.
        context
            The context object controls the environment and tags
            under which a request should execute resolvers.
        preview_deployment_id
            If specified, Chalk will route your request to the
            relevant preview deployment.

        Other Parameters
        ----------------
        query_name
            The name for class of query you're making, for example, "loan_application_model".
        correlation_id
            A globally unique ID for the query, used alongside logs and
            available in web interfaces. If None, a correlation ID will be
            generated for you and returned on the response.
        meta
            Arbitrary key:value pairs to associate with a query.

        Returns
        -------
        OnlineQueryResponseProtocol
            The outputs features and any query metadata,
            plus errors encountered while running the resolvers.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        ... ChalkClient().query(
        ...     input={User.name: "Katherine Johnson"},
        ...     output=[User.fico_score],
        ...     staleness={User.fico_score: "10m"},
        ... )
        """
        ...

    def upload_features(
        self,
        input: Mapping[Union[str, Feature, Any], Any],
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        """Upload data to Chalk for use in offline resolvers or to prime a cache.

        Parameters
        ----------
        input
            The features for which there are known values, mapped to those values.
        context
            The context object controls the environment and tags
            under which a request should execute resolvers.
        preview_deployment_id
            If specified, Chalk will route your request to the relevant preview deployment
        query_name
            Optionally associate this upload with a query name. See `.query` for more information.

        Other Parameters
        ----------------
        correlation_id
            A globally unique ID for this operation, used alongside logs and
            available in web interfaces. If None, a correlation ID will be
            generated for you and returned on the response.
        meta
            Arbitrary key:value pairs to associate with a query.

        Returns
        -------
        list[ChalkError] | None
            The errors encountered from uploading features.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> ChalkClient().upload_features(
        ...     input={User.id: 1, User.name: "Katherine Johnson"}
        ... )
        """
        ...

    def get_training_dataframe(
        self,
        input: Union[
            Mapping[Union[str, Feature], Sequence[Any]],
            pd.DataFrame,
            pl.DataFrame,
            DataFrame,
        ],
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        output_ts: bool = True,
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        max_samples: Optional[int] = None,
        disallow_stale_results: bool = False,
    ) -> pd.DataFrame:
        """Compute feature values from the offline store.
        See https://docs.chalk.ai/docs/training-client for more information.

        Parameters
        ----------
        input
            The features for which there are known values.
            It can be a mapping of features to a list of values for each
            feature, or an existing `DataFrame`.
            Each element in the `DataFrame` or list of values represents
            an observation in line with the timestamp in `input_times`.
        input_times
            A list of the times of the observations from `input`.
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row) in
            the resulting `DataFrame`, its value will be `None`.
        context
            The environment under which you'd like to query your data.
        dataset
            A unique name that if provided will be used to generate and
            save a dataset constructed from the list of features computed
            from the inputs.
        max_samples
            The maximum number of samples to include in the `DataFrame`.
            If not specified, all samples will be returned.

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.
        output_ts
            Whether to return the timestamp feature in a column
            named `__chalk__.CHALK_TS` in the resulting `DataFrame`.
        disallow_stale_results
            Whether to disallow stale results when running the query.
            By default, query results might not reflect ingested data
            from cron runs, migrations, or online resolvers in the
            last 30 minutes. Setting this flag to `True` will ensure
            that the latest data is read when running the query;
            however, doing so will significantly worsen query
            performance.

        Returns
        -------
        pd.DataFrame
            A `pandas.DataFrame` with columns equal to the names of the
            features in output, and values representing the value of the
            observation for each input time.
            The output maintains the ordering from `input`

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> sample_date = datetime.now() - timedelta(days=4)
        >>> user_ids = [1, 2, 3, 4]
        >>> X = ChalkClient().get_training_dataframe(
        ...     input={
        ...         User.id: user_ids,
        ...         User.ts: [sample_date for _ in user_ids],
        ...     },
        ...     output=[
        ...         User.id,
        ...         User.fullname,
        ...         User.email,
        ...         User.name_email_match_score,
        ...     ],
        ... )
        """
        ...

    def sample(
        self,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        output_id: bool = False,
        output_ts: bool = False,
        max_samples: Optional[int] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        context: Optional[OfflineQueryContext] = None,
        disallow_stale_results: bool = False,
    ) -> pd.DataFrame:
        """Get the most recent feature values from the offline store.

        See https://docs.chalk.ai/docs/training-client for more information.

        Parameters
        ----------
        output
            The features that you'd like to sample, if they exist.
            If an output feature was never computed for a sample (row)
            in the resulting `DataFrame`, its value will be `None`.
        max_samples
            The maximum number of rows to return.
        context
            The environment under which you'd like to query your data.

        Other Parameters
        ----------------
        required_output
            The features that you'd like to sample and must exist
            in each resulting row. Rows where a `required_output`
            was never stored in the offline store will be skipped.
            This differs from specifying the feature in `output`,
            where instead the row would be included, but the feature
            value would be `None`.
        output_ts
            Whether to return the timestamp feature in a column
            named `"__chalk__.CHALK_TS"` in the resulting `DataFrame`.
        output_id
            Whether to return the primary key feature in a column
            named `"__chalk__.__id__"` in the resulting `DataFrame`.
        disallow_stale_results
            Whether to disallow stale results when running the query.
            By default, query results might not reflect ingested data
            from cron runs, migrations, or online resolvers in the
            last 30 minutes. Setting this flag to `True` will ensure
            that the latest data is read when running the query;
            however, doing so will significantly worsen query
            performance.

        Returns
        -------
        pd.DataFrame
            A `pandas.DataFrame` with columns equal to the names of the features in output,
            and values representing the value of the most recent observation.

        Examples
        --------
        >>> from chalk.client import ChalkClient
        >>> sample_df = ChalkClient().sample(
        ...     output=[
        ...         Account.id,
        ...         Account.title,
        ...         Account.user.full_name
        ...     ],
        ...     max_samples=10
        ... )
        """
        ...
