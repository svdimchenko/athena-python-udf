import pytest

from athena_udf.utils import get_chunks, process_records


def test_get_chunks_empty():
    assert len(list(get_chunks([], 5))) == 0


def test_get_chunks_uneven():
    chunks = list(get_chunks([1, 2, 3], 2))
    assert chunks[0] == [1, 2]
    assert chunks[1] == [3]
    assert len(chunks) == 2


def test_get_chunks_more_elements_than_chunk():
    chunks = list(get_chunks([1, 2, 3], 4))
    assert chunks[0] == [1, 2, 3]
    assert len(chunks) == 1


# Test data
@pytest.fixture
def mock_records():
    return [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]


# Test cases using pytest.parametrize
@pytest.mark.parametrize(
    "func, args, mock_records, expected_output",
    [
        pytest.param(lambda *args: sum(mock_records), (1, 2), [3, 7, 11]),
        pytest.param(lambda *args: sum(mock_records()), (3, 4), [7, 11, 15]),
        pytest.param(lambda *args, records: "".join(args), (), ["helloworld", "foobar"]),
    ],
    indirect=["mock_records"],
)
def test_process_records(func, args, expected_output, mock_records):
    actual_output = process_records(func, args, mock_records)
    assert actual_output == expected_output


# Additional test case for empty records
def test_process_records_empty(mock_records):
    actual_output = process_records(lambda *args: sum(args), (1, 2), [])
    assert actual_output == []
