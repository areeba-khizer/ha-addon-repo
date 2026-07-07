import asyncio
import json
import logging
import os
import urllib.request
import argparse

import stats
import writer
from ha_client import connect_and_stream
from schema import to_raw

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

REPORT_INTERVAL = 600  # 10 minutes
_SENSOR_URL = "http://supervisor/core/api/states/sensor.ha_forwarder_bytes_10m"


def _post_sensor(bytes_count: int, records_count: int) -> None:
    token = os.getenv("SUPERVISOR_TOKEN", "")
    if not token:
        logger.debug("SUPERVISOR_TOKEN not set — skipping sensor update")
        return
    payload = json.dumps({
        "state": str(bytes_count),
        "attributes": {
            "unit_of_measurement": "B",
            "friendly_name": "Forwarder Upload (10 min)",
            "records_forwarded": records_count,
            "state_class": "measurement",
        },
    }).encode()
    req = urllib.request.Request(
        _SENSOR_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        logger.info(f"Upload sensor updated: {bytes_count}B / {records_count} records (HTTP {resp.status})")


async def _report_loop() -> None:
    while True:
        await asyncio.sleep(REPORT_INTERVAL)
        b, r = stats.take()
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, _post_sensor, b, r)
        except Exception as exc:
            logger.error(f"Sensor update failed: {exc}")


async def handle_event(event_data: dict) -> None:
    record = to_raw(event_data)
    if record is None:
        return
    await writer.write(record)


async def _run(duration: int) -> None:
    reporter = asyncio.create_task(_report_loop())
    try:
        if duration:
            logger.info(f"Will stop after {duration} seconds")
            try:
                await asyncio.wait_for(connect_and_stream(handle_event), timeout=duration)
            except asyncio.TimeoutError:
                logger.info(f"Duration of {duration}s reached — stopping")
        else:
            await connect_and_stream(handle_event)
    finally:
        reporter.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=0,
                        help="Stop after this many seconds (default: run forever)")
    args = parser.parse_args()

    logger.info("HA forwarder starting")
    asyncio.run(_run(args.duration))
