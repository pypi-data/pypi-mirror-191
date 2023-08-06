import os

import boto3
import boto3.session

# from botocore.config import Config

from mypy_boto3_s3 import (
    S3Client,
    S3ServiceResource,
)  # dev-dependency - TODO how to skip on build

AUTODL_S3_REGION = "us-east-1"


def init_s3(s3_host) -> S3ServiceResource:
    # TODO - we need to somehow include these in CLI without hardcoding

    # AWS_ACCESS_KEY_ID = os.environ["NEXT_PUBLIC_AWS_ACCESS_KEY_ID"]
    # AWS_SECRET_ACCESS_KEY = os.environ["NEXT_PUBLIC_AWS_SECRET_KEY"]
    AWS_ACCESS_KEY_ID = "AKIASO72NKUYW7ONNRFO"
    AWS_SECRET_ACCESS_KEY = "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"

    # is_using_localstack = "localhost" in s3_host

    # if not is_using_localstack:
    #     # TODO: clean up the whole codebase, so that we don't provide the s3_endpoint, unless we want to use localstack
    #     s3_host = None

    return boto3.resource(
        "s3",
        region_name=AUTODL_S3_REGION,
        endpoint_url=s3_host,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        # config=Config(s3={"use_accelerate_endpoint": not is_using_localstack}),
    )


def init_s3_client(s3_host) -> S3Client:
    return init_s3(s3_host).meta.client


_S3 = None

# TODO flatten and reorganize our S3 structure
# right now, there's three places that attempt to determine the target bucket
# and all of these stack upon each other in the resulting url:
# - this endpoint already includes the bucket name, so the bucket is predetermined for this endpoint
# - when calling S3.Bucket(name), we also provide another bucket name for the url
# - finally, the bucket name is appended to the s3_file_url attribute somewhere during the upload
def get_global_s3_resource():
    global _S3
    if _S3 is None:
        _S3 = init_s3(os.environ.get("NEXT_PUBLIC_AWS_S3_ENDPOINT"))

    return _S3
