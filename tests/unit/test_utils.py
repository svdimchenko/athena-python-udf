import pytest

from athena_udf.utils import (
    Record,
    get_chunks,
    process_records,
    process_records_in_chunks,
)


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
def mock_records_int():
    return [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]


@pytest.fixture
def mock_records_str():
    return [{"a": "a", "b": "b"}, {"a": "c", "b": "d"}, {"a": "e", "b": "f"}]


@pytest.mark.parametrize(("args", "expected_output"), [((1, 2), [6, 10, 14]), ((3, 4), [10, 14, 18])])
def test_process_records_sum(args: tuple, mock_records_int: list[Record], expected_output: list[int]):
    def mock_func(arg1: int, arg2: int, records: list[Record]) -> int:
        return sum(records) + arg1 + arg2

    actual_output = process_records(mock_func, args, mock_records_int)
    assert sorted(actual_output) == sorted(expected_output)


@pytest.mark.parametrize(
    ("args", "expected_output"), [(("x", "y"), ["abxy", "cdxy", "efxy"]), (("z", "w"), ["abzw", "cdzw", "efzw"])]
)
def test_process_records_concat(args: tuple, mock_records_str: list[Record], expected_output: list[str]):
    def mock_func(arg1, arg2, records: list[Record]) -> str:
        return "".join(records) + arg1 + arg2

    actual_output = process_records(mock_func, args, mock_records_str)
    assert sorted(actual_output) == sorted(expected_output)


@pytest.mark.parametrize(
    ("args", "chunk_size", "expected_output"),
    [
        ((1, 2), 1, [6, 10, 14]),
        ((1, 2), 2, [6, 10, 14]),
        ((1, 2), 3, [6, 10, 14]),
        ((3, 4), 1, [10, 14, 18]),
        ((3, 4), 2, [10, 14, 18]),
        ((3, 4), 3, [10, 14, 18]),
    ],
)
def test_process_records_in_chunks_sum(
    args: tuple, mock_records_int: list[Record], chunk_size: int, expected_output: list[int]
):
    def mock_func(arg1: int, arg2: int, records: list[Record]) -> int:
        return sum(records) + arg1 + arg2

    actual_output = process_records_in_chunks(mock_func, args, mock_records_int, chunk_size)
    assert sorted(actual_output) == sorted(expected_output)


@pytest.mark.parametrize(
    ("args", "chunk_size", "expected_output"),
    [
        (("x", "y"), 1, ["abxy", "cdxy", "efxy"]),
        (("x", "y"), 2, ["abxy", "cdxy", "efxy"]),
        (("x", "y"), 3, ["abxy", "cdxy", "efxy"]),
        (("z", "w"), 1, ["abzw", "cdzw", "efzw"]),
        (("z", "w"), 2, ["abzw", "cdzw", "efzw"]),
        (("z", "w"), 3, ["abzw", "cdzw", "efzw"]),
    ],
)
def test_process_records_in_chunks_concat(
    args: tuple, mock_records_str: list[Record], chunk_size: int, expected_output: list[str]
):
    def mock_func(arg1, arg2, records: list[Record]) -> str:
        return "".join(records) + arg1 + arg2

    actual_output = process_records_in_chunks(mock_func, args, mock_records_str, chunk_size)
    assert sorted(actual_output) == sorted(expected_output)
