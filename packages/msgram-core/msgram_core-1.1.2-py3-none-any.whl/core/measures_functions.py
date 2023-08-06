from typing import Dict

import numpy as np
import pandas as pd

from util.exceptions import ImplicitMetricValueError, InvalidMetricValue
from util.get_functions import create_coordinate_pair


def interpolate_series(series, x, y):
    """
    Interpolates a series using the given x and y values.

    This function interpolates a series using the given x and y values.
    """

    return [np.interp(item / 100, x, y) for item in series]


def resolve_metric_list_parameter(metric):
    """
    Resolves the metric list parameter to calculate a measure

    This functions converts the metric parameter to a pandas Series if it is a list (CalculateMeasures endpoint)
    otherwise it just returns the metric - already a pandas Series (Analysis endpoint).
    """
    return pd.Series(metric, dtype=np.float64) if isinstance(metric, list) else metric


def calculate_em1(data: Dict):
    """
    Calculates non-complex files density (em1).

    This function calculates non-complex files density measure (em1)
    used to assess the changeability quality sub characteristic.
    """
    files_complexity = resolve_metric_list_parameter(data["complexity"])
    files_functions = resolve_metric_list_parameter(data["functions"])

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]

    elif len(files_complexity) != len(files_functions):
        raise ImplicitMetricValueError(
            (
                "Unable to get the implicit value of metric `number_of_file` "
                "because the size of the lists of values of metrics `complexity` "
                "and `functions` are not equal."
            )
        )
    else:
        number_of_files = len(files_complexity)

    has_none = files_complexity is None or files_functions is None
    has_zero = len(files_complexity) == 0 or len(files_functions) == 0

    if has_none or has_zero:
        return 0

    COMPLEX_FILES_DENSITY_THRESHOLD = 10

    if files_complexity.sum() <= 0:
        raise InvalidMetricValue("The cyclomatic complexity of all files is lesser or equal than 0")

    if files_functions.sum() <= 0:
        raise InvalidMetricValue("The number of functions of all files is lesser or equal than 0")

    x, y = create_coordinate_pair(0, COMPLEX_FILES_DENSITY_THRESHOLD)

    files_in_thresholds_df = (files_complexity / files_functions) <= COMPLEX_FILES_DENSITY_THRESHOLD
    IF1 = np.interp(list(files_in_thresholds_df[(files_functions > 0)]), x, y)
    em1 = np.divide(sum(IF1), number_of_files)

    if np.isnan(em1) or np.isinf(em1):
        return 0
    return em1


def calculate_em2(data: Dict):
    """
    Calculates commented files density (em2).

    This function calculates commented files density measure (em2)
    used to assess the changeability quality sub characteristic.
    """
    files_comment_lines_density = resolve_metric_list_parameter(data["comment_lines_density"])

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]
    else:
        number_of_files = len(files_comment_lines_density)

    has_none = files_comment_lines_density is None
    has_zero = len(files_comment_lines_density) == 0

    if has_none or has_zero:
        return 0

    MINIMUM_COMMENT_DENSITY_THRESHOLD = 10
    MAXIMUM_COMMENT_DENSITY_THRESHOLD = 30

    if files_comment_lines_density.sum() < 0:
        raise InvalidMetricValue("The number of files comment lines density is lesser than 0")

    x, y = create_coordinate_pair(
        MINIMUM_COMMENT_DENSITY_THRESHOLD / 100, MAXIMUM_COMMENT_DENSITY_THRESHOLD / 100
    )

    files_between_thresholds = files_comment_lines_density[
        files_comment_lines_density.between(
            MINIMUM_COMMENT_DENSITY_THRESHOLD,
            MAXIMUM_COMMENT_DENSITY_THRESHOLD,
            inclusive="both",
        )
    ]

    em2i = interpolate_series(files_between_thresholds, x, y)
    em2 = np.divide(np.sum(em2i), number_of_files)

    if np.isnan(em2) or np.isinf(em2):
        return 0
    return em2


def calculate_em3(data: Dict):
    """
    Calculates duplicated files absence (em3).

    This function calculates the duplicated files absence measure (em3)
    used to assess the changeability quality sub characteristic.
    """
    files_duplicated_lines_density = resolve_metric_list_parameter(data["duplicated_lines_density"])

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]
    else:
        number_of_files = len(files_duplicated_lines_density)

    has_none = files_duplicated_lines_density is None
    has_zero = len(files_duplicated_lines_density) == 0

    if has_none or has_zero:
        return 0

    DUPLICATED_LINES_THRESHOLD = 5.0

    if files_duplicated_lines_density.sum() < 0:
        raise InvalidMetricValue("The number of files duplicated lines density is lesser than 0")

    x, y = create_coordinate_pair(0, DUPLICATED_LINES_THRESHOLD / 100)

    files_below_threshold = files_duplicated_lines_density[
        files_duplicated_lines_density <= DUPLICATED_LINES_THRESHOLD
    ]

    em3i = interpolate_series(files_below_threshold, x, y)
    em3 = np.divide(np.sum(em3i), number_of_files)

    if np.isnan(em3) or np.isinf(em3):
        return 0
    return em3


def calculate_em4(data: Dict[str, float]):
    """
    Calculates passed tests (em4)

    This function calculates the passed tests measure (em4)
    used to assess the testing status sub characteristic.
    """
    try:
        # number_of_tests está retornando valores incorretos
        number_of_tests = resolve_metric_list_parameter(data["tests"]).sum()
        number_of_test_errors = data["test_errors"]
        number_of_test_failures = data["test_failures"]

        x, y = create_coordinate_pair(0, 1, reverse_y=True)

        number_of_fail_tests = number_of_test_errors + number_of_test_failures
        if4i = np.divide((number_of_tests - number_of_fail_tests), number_of_tests)

    except ZeroDivisionError:
        return 0

    else:
        if np.isnan(if4i) or np.isinf(if4i):
            return 0
        return np.interp(if4i, x, y)


def calculate_em5(data: Dict[str, list]):
    """
    Calculates fast test builds (em5)

    This function calculates the fast test builds measure (em5)
    used to assess the testing status sub characteristic.
    """
    execution_time = resolve_metric_list_parameter(data["test_execution_time"])
    number_of_tests = resolve_metric_list_parameter(data["tests"])
    number_of_files = len(execution_time)

    has_none = execution_time is None or number_of_tests is None
    has_zero = len(execution_time) == 0 or len(number_of_tests) == 0

    if has_none or has_zero:
        return 0

    MAXIMUM_COVERAGE_THRESHOLD = 300000

    x, y = create_coordinate_pair(0, MAXIMUM_COVERAGE_THRESHOLD)

    execution_between_thresholds = execution_time[execution_time <= MAXIMUM_COVERAGE_THRESHOLD]
    fast_tests_between_thresholds = np.divide(execution_between_thresholds, number_of_tests)

    em5i = interpolate_series(fast_tests_between_thresholds, x, y)
    em5 = np.divide(np.sum(em5i), number_of_files)

    if np.isnan(em5) or np.isinf(em5):
        return 0

    return em5


def calculate_em6(data: Dict):
    """
    Calculates test coverage (em6).

    This function calculates the test coverage measure (em6)
    used to assess the testing status sub characteristic.
    """
    coverage = resolve_metric_list_parameter(data["coverage"])

    if "number_of_files" in data:
        number_of_files = data["number_of_files"]
    else:
        number_of_files = len(coverage)

    has_none = coverage is None
    has_zero = len(coverage) == 0

    if has_none or has_zero:
        return 0

    MINIMUM_COVERAGE_THRESHOLD = 60
    MAXIMUM_COVERAGE_THRESHOLD = 90

    x, y = create_coordinate_pair(
        MINIMUM_COVERAGE_THRESHOLD / 100,
        MAXIMUM_COVERAGE_THRESHOLD / 100,
        reverse_y=True,
    )

    files_between_thresholds = coverage[coverage >= MINIMUM_COVERAGE_THRESHOLD]
    em6i = interpolate_series(files_between_thresholds, x, y)
    em6 = np.divide(np.sum(em6i), number_of_files)

    if np.isnan(em6) or np.isinf(em6):
        return 0
    return em6


def calculate_em7(data: Dict):
    """
    Calculates team throughput (em7).

    This function calculates the team throughput measure (em7)
    used to assess the functional completeness subcharacteristic.
    """
    resolved_issues_with_us_label = data[
        "number_of_resolved_issues_with_US_label_in_the_last_x_days"
    ]

    total_issues_with_us_label = data["total_number_of_issues_with_US_label_in_the_last_x_days"]

    x, y = create_coordinate_pair(0, 1, reverse_y=True)

    if7 = np.divide(resolved_issues_with_us_label, total_issues_with_us_label)

    if np.isnan(if7) or np.isinf(if7):
        return 0
    return np.interp(if7, x, y)
