from typing import Optional, Tuple
from uuid import UUID, uuid4

from ._sbclient import connect_hub


def add_storage(root: str, account_handle: str) -> Tuple[Optional[UUID], Optional[str]]:
    from botocore.exceptions import ClientError

    hub = connect_hub()
    try:
        validate_root_arg(root)

        # get account
        data = (
            hub.table("account").select("*").eq("handle", account_handle).execute().data
        )
        account = data[0]

        # check if storage exists already
        response = hub.table("storage").select("*").eq("root", root).execute()
        if len(response.data) == 1:
            return response.data[0]["id"], None

        # add storage
        storage_region = get_storage_region(root)
        storage_type = get_storage_type(root)
        storage_fields = {
            "id": uuid4().hex,
            "account_id": account["id"],
            "root": root,
            "region": storage_region,
            "type": storage_type,
        }
        response = hub.table("storage").insert(storage_fields).execute()
        assert len(response.data) == 1

        return response.data[0]["id"], None
    except ClientError as exception:
        if exception.response["Error"]["Code"] == "NoSuchBucket":
            return None, "bucket-does-not-exists"
        else:
            return None, exception.response["Error"]["Message"]
    finally:
        hub.auth.sign_out()


def validate_root_arg(root: str) -> None:
    if not root.startswith(("s3://", "gs://")):
        raise ValueError("Only accept s3 and Google Cloud buckets.")


def get_storage_region(storage_root: str) -> Optional[str]:
    storage_root_str = str(storage_root)
    storage_region = None

    if storage_root_str.startswith("s3://"):
        import boto3

        response = boto3.client("s3").get_bucket_location(
            Bucket=storage_root_str.replace("s3://", "")
        )
        # returns `None` for us-east-1
        # returns a string like "eu-central-1" etc. for all other regions
        storage_region = response["LocationConstraint"]
        if storage_region is None:
            storage_region = "us-east-1"

    return storage_region


def get_storage_type(storage_root: str):
    if str(storage_root).startswith("s3://"):
        return "s3"
    elif str(storage_root).startswith("gs://"):
        return "gs"
    else:
        return "local"
