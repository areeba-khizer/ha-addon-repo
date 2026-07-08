# Changelog

All notable changes to the HA AWS Forwarder addon are documented here.

## [1.0.5] - 2026-07-08

### Added
- 10-minute upload stats sensor (`sensor.ha_forwarder_bytes_10m`) that tracks bytes and record count forwarded to AWS — visible and graphable in Home Assistant dashboards

### Fixed
- Default `ha_url` now correctly points to `http://supervisor/core` instead of a hardcoded IP address, so the addon works out of the box without manual URL configuration

### Security
- `aws_access_key_id` is now masked as a password field in the addon UI so it is no longer visible in plain text alongside the secret key

## [1.0.4] - 2026-07-07

### Fixed
- Default AWS region corrected from `us-east-1` to `eu-west-2`

## [1.0.3] - 2026-07-07

### Added
- New `ha_url` config option — lets you explicitly set the Home Assistant URL the addon connects to, useful if the Supervisor default does not work in your setup

## [1.0.2] - 2026-07-07

### Added
- New `ha_token` config option — lets you provide a long-lived HA token explicitly, as an alternative to relying solely on the Supervisor-injected token

## [1.0.1] - 2026-07-07

### Added
- Debug log on startup that confirms whether a Home Assistant token is present, making auth issues easier to diagnose in the addon logs

## [1.0.0] - 2026-07-07

### Added
- Stream Home Assistant state changes to **AWS Kinesis** or **AWS Firehose** in real time
- Configurable filtering: skip by domain (`ha_skip_domains`), skip by entity name pattern (`ha_skip_contains`), or allow only specific rooms (`ha_allow_rooms`)
- AWS credentials and region fully configurable via the addon UI
- Supervisor API integration — addon receives a valid HA token automatically via `homeassistant_api`
- Built on Python 3.12 (slim Docker image for fast startup and small footprint)
