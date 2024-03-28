import pandas as pd

import athena_udf


class PandasUDF(athena_udf.BaseAthenaUDF):

    @staticmethod
    def handle_athena_record(input_schema, output_schema, arguments):
        list_of_data = arguments[0]
        series = pd.Series(list_of_data)
        return list(series.pct_change())


lambda_handler = PandasUDF().lambda_handler
