# HA AWS Forwarder — Add-on Repository

Custom Home Assistant add-on repository containing the **HA AWS Forwarder** add-on.

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store**
2. Click the **⋮** menu (top right) → **Repositories**
3. Add this repository URL and click **Add**
4. Find **HA AWS Forwarder** in the store and click **Install**

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
