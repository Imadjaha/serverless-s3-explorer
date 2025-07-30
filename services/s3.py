import os
import boto3
from functools import lru_cache
from botocore.config import Config

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
_s3_global = boto3.client("s3", region_name=AWS_REGION)


@lru_cache(maxsize=None)
def client_for(bucket: str):
    """Return an S3 client in the bucket’s home region (cached)."""
    region = (
        _s3_global.get_bucket_location(Bucket=bucket).get("LocationConstraint")
        or "us-east-1"
    )
    return boto3.client(
        "s3", region_name=region, config=Config(signature_version="s3v4")
    )


def list_buckets():
    return _s3_global.list_buckets()["Buckets"]


@lru_cache(maxsize=None)
def count_keys(bucket: str, prefix: str, flt: str | None):
    """Count objects under *prefix* whose key contains *flt* (case‑insensitive)."""
    s3 = client_for(bucket)
    total = 0
    for page in s3.get_paginator("list_objects_v2").paginate(
        Bucket=bucket, Prefix=prefix
    ):
        for obj in page.get("Contents", []):
            if not flt or flt in obj["Key"].lower():
                total += 1
    return total
