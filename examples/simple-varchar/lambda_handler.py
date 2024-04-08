from typing import Any

from pyarrow import Schema

from athena_udf import BaseAthenaUDF


class SimpleVarcharUDF(BaseAthenaUDF):

    @staticmethod
    def handle_athena_record(input_schema: Schema, output_schema: Schema, arguments: list[Any]):
        varchar = arguments[0]
        return varchar.lower()


lambda_handler = SimpleVarcharUDF(use_threads=False).lambda_handler
