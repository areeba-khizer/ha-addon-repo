#!/bin/sh

# HA_URL and HA_TOKEN are read from /data/options.json by config.py
# SUPERVISOR_TOKEN is kept as a fallback in case ha_token option is left blank
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"

exec python3 /app/main.py
