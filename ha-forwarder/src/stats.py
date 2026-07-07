import threading

_lock = threading.Lock()
_bytes = 0
_records = 0


def add(byte_count: int) -> None:
    global _bytes, _records
    with _lock:
        _bytes += byte_count
        _records += 1


def take() -> tuple[int, int]:
    """Returns (bytes, records) accumulated since last call, then resets both."""
    global _bytes, _records
    with _lock:
        b, r = _bytes, _records
        _bytes = 0
        _records = 0
    return b, r
