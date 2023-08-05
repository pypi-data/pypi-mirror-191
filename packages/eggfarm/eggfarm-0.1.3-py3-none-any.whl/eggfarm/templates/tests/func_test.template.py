from {{ func_name }} import {{ func_class }}
from stonewave.sql.udtfs.test_utility import (
    check_expected_parameters_list,
    eval_table_function_test,
)
from tests.supported_signature_list import supported_signature_list
import pytest


def _execute_function(args):
    func_expected_params = supported_signature_list()
    check_expected_parameters_list(func_expected_params)

    batch_iterator = eval_table_function_test(
        {{ func_class }}, args, func_expected_params
    )
    return list(batch_iterator)


def _assert_add_two(num1, num2, expected_result):
    args = [num1, num2]
    batches = _execute_function(args)
    assert len(batches) == 1
    batch = batches[0]
    assert batch.num_rows == 1
    assert batch.num_columns == 1
    assert batch.schema.names == ["add_result"]
    results = batch[batch.schema.get_field_index("add_result")][0].as_py()
    # write_row method will make all results as string type
    assert str(results) == str(expected_result)


def test_add_two():
    _assert_add_two(3, 5, 8)
    _assert_add_two(10, 12, 22)