import asyncio
import json
import logging
from typing import Awaitable, Callable

import websockets
from websockets.exceptions import ConnectionClosed

from config import HA_ALLOW_ROOMS, HA_SKIP_CONTAINS, HA_SKIP_DOMAINS, HA_TOKEN, HA_URL

logger = logging.getLogger(__name__)


def _ws_url(ha_url: str) -> str:
    return ha_url.rstrip("/").replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"


def _should_forward(entity_id: str, domain: str) -> bool:
    if domain in HA_SKIP_DOMAINS:
        return False
    if any(s in entity_id for s in HA_SKIP_CONTAINS):
        return False
    if HA_ALLOW_ROOMS and not any(r in entity_id for r in HA_ALLOW_ROOMS):
        return False
    return True


async def connect_and_stream(on_event: Callable[[dict], Awaitable[None]]) -> None:
    url = _ws_url(HA_URL)

    while True:
        try:
            logger.info(f"Connecting to {url}")
            async with websockets.connect(url) as ws:

                msg = json.loads(await ws.recv())
                if msg.get("type") != "auth_required":
                    raise ValueError(f"Expected auth_required, got: {msg}")

                await ws.send(json.dumps({"type": "auth", "access_token": HA_TOKEN}))
                msg = json.loads(await ws.recv())
                if msg.get("type") != "auth_ok":
                    raise ValueError(f"Authentication failed: {msg}")
                logger.info("Authenticated with Home Assistant")

                await ws.send(json.dumps({"id": 1, "type": "subscribe_events", "event_type": "state_changed"}))
                msg = json.loads(await ws.recv())
                if not msg.get("success"):
                    raise ValueError(f"Subscription failed: {msg}")
                logger.info("Subscribed to state_changed — streaming events")

                async for raw in ws:
                    msg = json.loads(raw)
                    if msg.get("type") != "event":
                        continue

                    event_data = msg.get("event", {}).get("data", {})
                    entity_id = event_data.get("entity_id", "")
                    domain = entity_id.split(".")[0] if "." in entity_id else ""

                    if _should_forward(entity_id, domain):
                        await on_event(event_data)

        except ConnectionClosed as exc:
            logger.warning(f"Connection closed ({exc}). Reconnecting in 5s...")
            await asyncio.sleep(5)
        except Exception as exc:
            logger.error(f"Unexpected error: {exc}. Reconnecting in 10s...")
            await asyncio.sleep(10)
