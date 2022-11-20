from typing import Union
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.execution_engine import ExecutionEngine
from great_expectations.expectations.expectation import (
    ExpectationValidationResult,
    QueryExpectation,
)


class ExpectQueriedColumnToBeUniqueWithCondition(QueryExpectation):
    """ Expect column values to be distinct, with an filter.
        column A - the column to check uniqueness
        column B - the filter - if boolean column, provide just the column name (evaluated to True) """
    metric_dependencies = ("query.column_pair",)

    query = """
            SELECT {column_A}, COUNT(1)
            FROM {active_batch}
            WHERE {column_B}
            GROUP BY {column_A}
            HAVING count(1) > 1
            """

    success_keys = (
        "column_A",
        "column_B",
        "query",
    )

    domain_keys = ("batch_id", "row_condition", "condition_parser")
    default_kwarg_values = {
        "result_format": "BASIC",
        "include_config": True,
        "catch_exceptions": False,
        "meta": None,
        "column": None,
        "query": query,
    }

    def _validate(
        self,
        configuration: ExpectationConfiguration,
        metrics: dict,
        runtime_configuration: dict = None,
        execution_engine: ExecutionEngine = None,
    ) -> Union[ExpectationValidationResult, dict]:

        query_result = metrics.get("query.column_pair")
        query_result = dict(query_result)
        if not query_result:
            return {
                "success": True}

        else:
            return {
            "success": False,
            "result": {"observed_value": query_result},
        }

    examples = [
        {
            "data": [
                {
                    "dataset_name": "test",
                    "data": {
                        "uuid": [1, 2, 2, 3, 4, 4],
                        "is_open": [True, False, True, True, True, True],
                        "is_open_2": [False, True, False, False, False, True]
                    },
                },
            ],
            "tests": [
                {
                    "title": "basic_negative_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {
                        "column_A": "uuid",
                        "column_B": "is_open"
                    },
                    "out": {"success": False},
                    "only_for": ["sqlite"],
                },
                {
                    "title": "basic_positive_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {
                        "column_A": "uuid",
                        "column_B": "is_open_2"
                    },
                    "out": {"success": True},
                    "only_for": ["sqlite"],
                }
            ]}]

    # This dictionary contains metadata for display in the public gallery
    library_metadata = {
        "tags": ["query-based"],
        "contributors": ["@itaise"],
    }


if __name__ == "__main__":
    ExpectQueriedColumnToBeUniqueWithCondition().print_diagnostic_checklist()