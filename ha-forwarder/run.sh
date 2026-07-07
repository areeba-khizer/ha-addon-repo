#!/bin/sh

# HA connection — Supervisor injects SUPERVISOR_TOKEN automatically
export HA_URL="http://supervisor/core"
export HA_TOKEN="${SUPERVISOR_TOKEN}"

exec python3 /app/main.py
