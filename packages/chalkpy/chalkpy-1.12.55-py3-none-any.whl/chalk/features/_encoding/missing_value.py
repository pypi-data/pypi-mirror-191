from typing import Literal, Union

MissingValueStrategy = Union[
    Literal["error"],  # Raise a TypeError if missing values are found
    # Coerce missing values to the default value for the feature, if one is defined. Otherwise, raise a TypeError
    Literal["default_or_error"],
    # Coerce missing values to the default value for the feature, if one is defined. Otherwise, treat missing values as valid.
    Literal["default_or_allow"],
    Literal["allow"],  # Treat missing values as valid values
]
