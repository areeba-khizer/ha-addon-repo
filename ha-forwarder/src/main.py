import asyncio
import logging
import argparse

import writer
from ha_client import connect_and_stream
from schema import to_raw

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


async def handle_event(event_data: dict) -> None:
    record = to_raw(event_data)
    if record is None:
        return
    await writer.write(record)


async def _run(duration: int) -> None:
    if duration:
        logger.info(f"Will stop after {duration} seconds")
        try:
            await asyncio.wait_for(connect_and_stream(handle_event), timeout=duration)
        except asyncio.TimeoutError:
            logger.info(f"Duration of {duration}s reached — stopping")
    else:
        await connect_and_stream(handle_event)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=0,
                        help="Stop after this many seconds (default: run forever)")
    args = parser.parse_args()

    logger.info("HA forwarder starting")
    from config import HA_URL, HA_TOKEN
    logger.info(f"HA_URL={HA_URL}  token_present={'yes' if HA_TOKEN else 'NO - token is empty'}")
    asyncio.run(_run(args.duration))
