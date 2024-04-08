from typing import Any

import pyarrow as pa

from athena_udf import BaseAthenaUDF


class MultithreadUDF(BaseAthenaUDF):

    @staticmethod
    def handle_athena_record(input_schema: pa.Schema, output_schema: pa.Schema, arguments: list[Any]):
        varchar = arguments[0]
        return varchar.lower()


lambda_handler = MultithreadUDF().lambda_handler
