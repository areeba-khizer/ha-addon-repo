from datetime import datetime, timezone
from typing import Optional

_SKIP_STATES = {"unavailable", "unknown", ""}


def to_raw(event_data: dict) -> Optional[dict]:
    new_state = event_data.get("new_state")
    if not new_state:
        return None
    if new_state.get("state", "") in _SKIP_STATES:
        return None

    return {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        **event_data,
    }
