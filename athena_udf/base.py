import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from uuid import uuid4

import pyarrow as pa

from athena_udf.utils import get_chunks


class BaseAthenaUDF:

    def __init__(self, chunk_size: Optional[int] = None):
        self.chunk_size = chunk_size

    @staticmethod
    def handle_ping(event):
        return {
            "@type": "PingResponse",
            "catalogName": "event",
            "queryId": event["queryId"],
            "sourceType": "athena_udf",
            "capabilities": 23,
        }

    def lambda_handler(self, event, context):
        incoming_type = event["@type"]
        if incoming_type == "PingRequest":
            return self.handle_ping(event)
        elif incoming_type == "UserDefinedFunctionRequest":
            return self.handle_udf_request(event)

        raise Exception(f"Unknown event type {incoming_type} from Athena")

    def handle_udf_request(self, event):
        input_schema = pa.ipc.read_schema(pa.BufferReader(base64.b64decode(event["inputRecords"]["schema"])))
        output_schema = pa.ipc.read_schema(pa.BufferReader(base64.b64decode(event["outputSchema"]["schema"])))
        record_batch = pa.ipc.read_record_batch(
            pa.BufferReader(base64.b64decode(event["inputRecords"]["records"])),
            input_schema,
        )
        record_batch_list = record_batch.to_pylist()

        outputs = []
        with ThreadPoolExecutor() as executor:
            if self.chunk_size is None:
                futures = [
                    executor.submit(self.handle_athena_record, input_schema, output_schema, list(record.values()))
                    for record in record_batch_list
                ]
                for future in as_completed(futures):
                    outputs.append(future.result())
            else:
                futures = [
                    [
                        executor.submit(self.handle_athena_record, input_schema, output_schema, list(record.values()))
                        for record in batch
                    ]
                    for batch in get_chunks(record_batch_list, self.chunk_size)
                ]
                for future_batch in futures:
                    for future in as_completed(future_batch):
                        outputs.append(future.result())
        return {
            "@type": "UserDefinedFunctionResponse",
            "records": {
                "aId": str(uuid4()),
                "schema": event["outputSchema"]["schema"],
                "records": base64.b64encode(
                    pa.RecordBatch.from_arrays([outputs], schema=output_schema).serialize()
                ).decode(),
            },
            "methodName": event["methodName"],
        }

    @staticmethod
    def handle_athena_record(input_schema, output_schema, arguments):
        raise NotImplementedError()
