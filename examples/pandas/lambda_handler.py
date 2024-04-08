import pandas as pd

from athena_udf import BaseAthenaUDF


class PandasUDF(BaseAthenaUDF):

    @staticmethod
    def handle_athena_record(input_schema, output_schema, arguments):
        list_of_data = arguments[0]
        series = pd.Series(list_of_data)
        return list(series.pct_change())


lambda_handler = PandasUDF(use_threads=False).lambda_handler
