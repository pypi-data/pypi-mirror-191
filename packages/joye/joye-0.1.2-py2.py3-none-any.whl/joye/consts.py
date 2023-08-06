import os

# mock access key & secret for data
DATA_MODE = "mock"
if os.environ.get("DATA_ACCESS_KEY_ID"):
    DATA_MODE = "real"
DATA_ACCESS_KEY_ID = os.environ.get("DATA_ACCESS_KEY_ID") or "LTAI5t7djehb5EpCQXMtjqBi"
DATA_ACCESS_KEY_SECRET = (
    os.environ.get("DATA_ACCESS_KEY_SECRET") or "AuJDq8kVJ38i2vYaOxrV1iGHcctoer"
)
DATA_ENDPOINT = (
    os.environ.get("DATA_ENDPOINT") or "https://oss-cn-shanghai.aliyuncs.com"
)
DATA_BUCKET = "jqy-data"

# mock access key & secret for strategy
STRATEGY_MODE = "mock"
if os.environ.get("STRATEGY_ACCESS_KEY_ID"):
    STRATEGY_MODE = "real"
STRATEGY_ACCESS_KEY_ID = (
    os.environ.get("STRATEGY_ACCESS_KEY_ID") or "LTAI5tCX19zauFf7AFa6eVxV"
)
STRATEGY_ACCESS_KEY_SECRET = (
    os.environ.get("STRATEGY_ACCESS_KEY_SECRET") or "lkIFusuUcL6z2pBVY0myDMS4wVfjSE"
)
STRATEGY_ENDPOINT = (
    os.environ.get("STRATEGY_ENDPOINT") or "https://oss-cn-shanghai.aliyuncs.com"
)
STRATEGY_BUCKET = "jqy-strategy2"
