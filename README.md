# athena-python-udf

<!-- markdownlint-disable -->
[![PyPI](https://img.shields.io/pypi/v/athena-udf.svg)](https://pypi.org/project/athena-udf/)
[![Changelog](https://img.shields.io/github/v/release/dmarkey/python-athena-udf?include_prereleases&label=changelog)](https://github.com/dmarkey/python-athena-udf/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dmarkey/python-athena-udf/blob/main/LICENSE)
<!-- markdownlint-restore -->

Athena User Defined Functions(UDFs) in Python made easy!

This library implements the Athena UDF protocol in Python,
so you don't have to use Java, and you can use any Python library you wish, including numpy/pandas!

## Installation

Install this library using `pip`:

```bash
pip install athena-python-udf
```

## Usage

- Install the package
- Create a lambda handler Python file subclass `BaseAthenaUDF`
- Implement the `handle_athena_record` static method with your required functionality like this:

```python
from typing import Any

from athena_udf import BaseAthenaUDF
from pyarrow import Schema


class SimpleVarcharUDF(BaseAthenaUDF):

    @staticmethod
    def handle_athena_record(input_schema: Schema, output_schema: Schema, arguments: list[Any]):
        varchar = arguments[0]
        return varchar.lower()


lambda_handler = SimpleVarcharUDF(use_threads=False).lambda_handler
```

This very basic example takes a `varchar` input, and returns the lowercase version.

- `varchar` is converted to a python string on the way in and way out.
- `input_schema` contains a `PyArrow` schema representing the schema of the data being passed
- `output_schema` contains a `PyArrow` schema representing the schema of what athena expects to be returned.
- `arguments` contains a list of arguments given to the function. Can be more than one with different types.

You can also play with multithreading (enabled by default) using the following parameters:

- `chunk_size` - if you want to force splitting received record batch into chunks of specific size
  and process these chunks consecutively.
  It may be useful if your lambda will operate with some rate-limited external APIs.

- `max_workers` - basic ThreadPoolExecutor parameter. You can leave it empty to keep default behavior.

If you package the above into a zip, with dependencies and name your lambda function `my-lambda`
you can then run it from the athena console like so:

```sql
USING EXTERNAL FUNCTION my_udf(col1 varchar) RETURNS varchar LAMBDA 'athena-test'

SELECT my_udf('FooBar');
```

Which will yield the result `foobar`

See other examples in the [examples](examples) folder of this repo.

## Important information before using

Each lambda instance will take multiple requests for the same query.
Each request can contain multiple rows, `athena-udf`
handles this for you and your implementation will receive a single row.

Athena will group your data into around 1MB chunks in a single request.
The maximum your function can return is 6MB per chunk.

This library uses `PyArrow`. This is a large library, so the Lambdas will be around 50MB zipped.

Timestamps seem to be truncated into Python `date` objects missing the time.

Functions can return one value only.
To return more complex data structures, consider returning a JSON payload and parsing on athena.

## Development

To contribute to this library, first checkout the code.
Then create a new virtual environment with all required dependencies and activate it:

```bash
poetry install
source .venv/bin/activate
```

To run the tests:

```bash
pytest
```
