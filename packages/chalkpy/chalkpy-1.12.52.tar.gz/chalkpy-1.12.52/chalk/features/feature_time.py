from datetime import datetime
from typing import Any

from typing_extensions import Annotated

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import unwrap_feature

FeatureTime = Annotated[datetime, "__chalk_ts__"]
"""Marker for a FeatureTime.

>>> from chalk.features import features
>>> @features
... class User:
...     updated_at: FeatureTime
"""


def feature_time() -> Any:
    """Declare a FeatureTime (deprecated).

    Deprecated in favor of
    >>> from chalk.features import features
    >>> @features
    ... class User:
    ...     updated_at: FeatureTime
    """
    return Feature(typ=datetime, is_feature_time=True)


def is_feature_time(f: Any) -> bool:
    """Determine whether a feature is a feature time.

    Parameters
    ----------
    f
        A feature (i.e. User.ts)

    Returns
    -------
    bool
        True if the feature is a `FeatureTime` and False otherwise
    """
    return unwrap_feature(f).is_feature_time
