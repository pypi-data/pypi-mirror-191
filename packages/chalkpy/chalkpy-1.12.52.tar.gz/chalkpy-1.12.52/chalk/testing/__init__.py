from chalk.features import DataFrame
from chalk.utils.missing_dependency import missing_dependency_exception


def assert_frame_equal(
    left: DataFrame,
    right: DataFrame,
    check_column_order: bool = True,
    check_row_order: bool = True,
):
    """Given two ``DataFrame``s, `left` and `right`, check if `left == right`,
    and raise otherwise.

    Parameters
    ----------
    left
        The dataframe to compare.
    right
        The dataframe to compare with.
    check_column_order
        If False, allows the assert/test to succeed if the required columns are present,
        irrespective of the order in which they appear.
    check_row_order
        If False, allows the assert/test to succeed if the required rows are present,
        irrespective of the order in which they appear; as this requires
        sorting, you cannot set on frames that contain unsortable columns.

    Raises
    ------
    AssertionError
        If `left` does not equal `right`
    """
    try:
        import polars.testing
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    return polars.testing.assert_frame_equal(
        left.to_polars().collect(),
        right.to_polars().collect(),
        check_row_order=check_row_order,
        check_column_order=check_column_order,
    )
