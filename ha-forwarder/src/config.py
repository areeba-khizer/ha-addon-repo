import os

HA_URL = os.environ["HA_URL"]
HA_TOKEN = os.environ["HA_TOKEN"]
HA_SKIP_DOMAINS = set(
    d.strip() for d in os.getenv("HA_SKIP_DOMAINS", "").split(",") if d.strip()
)
HA_ALLOW_ROOMS = [
    r.strip() for r in os.getenv("HA_ALLOW_ROOMS", "").split(",") if r.strip()
]
HA_SKIP_CONTAINS = [
    s.strip() for s in os.getenv("HA_SKIP_CONTAINS", "").split(",") if s.strip()
]

AWS_REGION = os.getenv("AWS_REGION", "")
OUTPUT_TARGET = os.getenv("OUTPUT_TARGET", "firehose")
FIREHOSE_DELIVERY_STREAM = os.getenv("FIREHOSE_DELIVERY_STREAM", "")
KINESIS_STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "")
