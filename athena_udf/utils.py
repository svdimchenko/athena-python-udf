from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, TypeVar

T = TypeVar("T")
Record = dict[str, ...]


def get_chunks(lst: list[T], n: int) -> Generator[list[T], None, None]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def process_records(func: Callable[..., T], args: tuple, records: list[Record]) -> list[T]:
    """Process args with callable using ThreadPoolExecutor."""
    with ThreadPoolExecutor() as executor:
        return [
            future.result()
            for future in as_completed([executor.submit(func, *args, list(record.values())) for record in records])
        ]


def process_records_in_chunks(func: Callable[..., T], args: tuple, records: list[Record], chunk_size: int) -> list[T]:
    """Process args with callable using ThreadPoolExecutor."""
    outputs = []
    with ThreadPoolExecutor() as executor:
        futures = [
            [executor.submit(func, *args, list(record.values())) for record in batch]
            for batch in get_chunks(records, chunk_size)
        ]
        for future_batch in futures:
            outputs.extend([future.result() for future in as_completed(future_batch)])
    return outputs
