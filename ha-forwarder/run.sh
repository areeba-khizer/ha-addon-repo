#!/bin/sh

# HA_URL is read from /data/options.json by config.py
# SUPERVISOR_TOKEN is injected by Supervisor via homeassistant_api and used directly
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"

exec python3 /app/main.py
