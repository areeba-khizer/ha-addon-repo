import json
import os
from pathlib import Path

# Inside the HA add-on, Supervisor writes the Configuration tab values here
_OPTIONS_FILE = Path("/data/options.json")


def _opt(key: str, default: str = "") -> str:
    if _OPTIONS_FILE.exists():
        with open(_OPTIONS_FILE) as f:
            return str(json.load(f).get(key, default))
    return os.getenv(key.upper(), default)


# HA connection — read from add-on options, fall back to env vars for local dev
HA_URL = _opt("ha_url") or os.environ.get("HA_URL", "http://supervisor/core")
HA_TOKEN = os.environ.get("HA_TOKEN") or os.environ.get("SUPERVISOR_TOKEN", "")

HA_SKIP_DOMAINS = set(d.strip() for d in _opt("ha_skip_domains").split(",") if d.strip())
HA_ALLOW_ROOMS = [r.strip() for r in _opt("ha_allow_rooms").split(",") if r.strip()]
HA_SKIP_CONTAINS = [s.strip() for s in _opt("ha_skip_contains").split(",") if s.strip()]

AWS_REGION = _opt("aws_region")
AWS_ACCESS_KEY_ID = _opt("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = _opt("aws_secret_access_key")
OUTPUT_TARGET = _opt("output_target", "firehose")
FIREHOSE_DELIVERY_STREAM = _opt("firehose_delivery_stream")
KINESIS_STREAM_NAME = _opt("kinesis_stream_name")
