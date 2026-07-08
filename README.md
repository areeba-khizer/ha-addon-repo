# HA AWS Forwarder — Add-on Repository

Custom Home Assistant add-on repository containing the **HA AWS Forwarder** add-on.

```
┌──────────────────────────────────────┐
│           Home Assistant             │
│                                      │
│  light.living_room ──────────────►   │
│  sensor.temperature ─────────────►   │  state changes
│  binary_sensor.motion ───────────►   │  via WebSocket
└─────────────────────┬────────────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │   HA AWS Forwarder  │
           │       Add-on        │
           │                     │
           │  filter by domain   │
           │  filter by room     │
           │  filter by entity   │
           └────────┬────────────┘
                    │
          ┌─────────┴──────────┐
          │                    │
          ▼                    ▼
  ┌───────────────┐   ┌────────────────┐
  │    Kinesis    │   │    Firehose    │
  │  Data Streams │   │    Delivery    │
  └───────────────┘   └───────┬────────┘
                              │
                              ▼
                     ┌────────────────┐
                     │  S3 / Redshift │
                     │  / OpenSearch  │
                     └────────────────┘
```

## Installation

1. Go to **Settings** → **Add-ons**
2. Click **Add-on Store** — if you don't see it directly, look for an **Install Add-on** button (the label varies slightly by HA version)
3. In the **top-right corner**, click the **⋮** (three dots) → **Repositories**
4. Paste this URL and click **Add**:
   `https://github.com/areeba-khizer/ha-addon-repo`
5. Close the dialog — the **HA AWS Forwarder** card will appear in the store. Click it → **Install**

## Configuration

After installing, open the add-on's **Configuration** tab and fill in:

| Option | Description |
|--------|-------------|
| `aws_region` | Your AWS region (e.g. `us-east-1`) |
| `aws_access_key_id` | IAM access key ID |
| `aws_secret_access_key` | IAM secret access key (stored masked) |
| `output_target` | `firehose` or `kinesis` |
| `firehose_delivery_stream` | Firehose stream name (if using firehose) |
| `kinesis_stream_name` | Kinesis stream name (if using kinesis) |
| `ha_skip_domains` | Comma-separated domains to ignore |
| `ha_skip_contains` | Comma-separated substrings to ignore in entity IDs |
| `ha_allow_rooms` | Comma-separated room names to allow (empty = all rooms) |

No credentials are stored in this repository.
