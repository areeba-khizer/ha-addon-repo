#!/usr/bin/env bashio

# AWS credentials — entered in the add-on Configuration tab, never stored in the repo
export AWS_ACCESS_KEY_ID="$(bashio::config 'aws_access_key_id')"
export AWS_SECRET_ACCESS_KEY="$(bashio::config 'aws_secret_access_key')"
export AWS_REGION="$(bashio::config 'aws_region')"

# AWS destination
export OUTPUT_TARGET="$(bashio::config 'output_target')"
export FIREHOSE_DELIVERY_STREAM="$(bashio::config 'firehose_delivery_stream')"
export KINESIS_STREAM_NAME="$(bashio::config 'kinesis_stream_name')"

# HA event filters
export HA_SKIP_DOMAINS="$(bashio::config 'ha_skip_domains')"
export HA_SKIP_CONTAINS="$(bashio::config 'ha_skip_contains')"
export HA_ALLOW_ROOMS="$(bashio::config 'ha_allow_rooms')"

# HA connection — Supervisor injects these automatically, no user input needed
export HA_URL="http://supervisor/core"
export HA_TOKEN="${SUPERVISOR_TOKEN}"

exec python3 /app/main.py
