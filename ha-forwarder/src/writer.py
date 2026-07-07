import asyncio
import json
import logging

import boto3

import stats
from config import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, FIREHOSE_DELIVERY_STREAM, KINESIS_STREAM_NAME, OUTPUT_TARGET

logger = logging.getLogger(__name__)

_client = None


# Creates the boto3 client once and reuses it — returns None when AWS is not configured
def _get_client():
    global _client
    if _client is None and AWS_REGION:
        service = "firehose" if OUTPUT_TARGET == "firehose" else "kinesis"
        _client = boto3.client(
            service,
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY or None,
        )
    return _client


# Blocking send — runs in a background thread so it never freezes the event loop
def _send(record: dict) -> None:
    data = (json.dumps(record) + "\n").encode("utf-8")
    stats.add(len(data))
    client = _get_client()

    if client is None:
        logger.info(f"[STUB] {record.get('ingested_at')}  {record.get('entity_id')}  {record.get('new_state', {}).get('state')}")
        return

    if OUTPUT_TARGET == "firehose":
        if not FIREHOSE_DELIVERY_STREAM:
            raise ValueError("FIREHOSE_DELIVERY_STREAM is not configured in the add-on options")
        client.put_record(DeliveryStreamName=FIREHOSE_DELIVERY_STREAM, Record={"Data": data})
        logger.debug(f"→ Firehose: {record.get('entity_id')}")

    elif OUTPUT_TARGET == "kinesis":
        if not KINESIS_STREAM_NAME:
            raise ValueError("KINESIS_STREAM_NAME is not configured in the add-on options")
        client.put_record(StreamName=KINESIS_STREAM_NAME, Data=data, PartitionKey=record.get("entity_id", "default"))
        logger.debug(f"→ Kinesis: {record.get('entity_id')}")

    else:
        raise ValueError(f"Unknown OUTPUT_TARGET: {OUTPUT_TARGET!r} — use 'firehose' or 'kinesis'")


# Async wrapper — hands the blocking send off to a thread so concurrent events are sent in parallel
async def write(record: dict) -> None:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send, record)
