"""Initializing an instance.

This functionality will at first only be accessible through Python API client & CLI.

We might also enable it from the UI.
"""
from pathlib import Path
from typing import Mapping, Optional
from uuid import UUID, uuid4

from postgrest.exceptions import APIError

from lnhub_rest._add_storage import add_storage
from lnhub_rest._assets import schemas as known_schema_names
from lnhub_rest._sbclient import connect_hub_with_auth


def init_instance(
    *,
    owner: str,  # owner handle
    name: str,  # instance name
    storage: str,  # storage location on cloud
    db: Optional[str] = None,  # str has to be postgresdsn (use pydantic in the future)
    schema: Optional[str] = None,  # comma-separated list of schema names
    # replace with token-based approach!
    _email: Optional[str] = None,
    _password: Optional[str] = None,
) -> Optional[str]:
    hub = connect_hub_with_auth(email=_email, password=_password)
    try:
        # validate input arguments
        schema_str = validate_schema_arg(schema)
        # validate_storage_arg(storage)  # needs improvement! happens in add_storage
        validate_db_arg(db)

        # get account
        data = hub.table("account").select("*").eq("handle", owner).execute().data
        account = data[0]

        # get storage and add if not yet there
        storage_id, message = add_storage(storage, account_handle=account["handle"])
        if message is not None:
            return message
        assert storage_id is not None

        response = (
            hub.table("instance")
            .select("*")
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
        )
        if len(response.data) > 0:
            return "instance-exists-already"

        validate_unique_sqlite(
            hub=hub, db=db, storage_id=storage_id, name=name, account=account
        )

        instance_id = uuid4().hex

        instance_fields = {
            "id": instance_id,
            "account_id": account["id"],
            "name": name,
            "storage_id": storage_id,
            "db": db,
            "schema_str": schema_str,
            "public": False,  # hard-code for now
        }
        data = hub.table("instance").insert(instance_fields).execute().data
        assert len(data) == 1

        account_instance_fields = {
            "instance_id": instance_id,
            "account_id": account["id"],
            "permission": "admin",
        }
        data = (
            hub.table("account_instance").insert(account_instance_fields).execute().data
        )
        assert len(data) == 1
        # upon successful insert of a new row in the instance table
        # (and all associated tables), return None
        # clients test for this return value, hence, don't change it
        return None
    except APIError as api_error:
        uq_instance_db_error = (
            'duplicate key value violates unique constraint "uq_instance_db"'
        )
        if api_error.message == uq_instance_db_error:
            return "db-already-exists"
        return str(api_error)
    except Exception as e:
        return str(e)
    finally:
        hub.auth.sign_out()


def validate_schema_arg(schema: Optional[str] = None) -> str:
    if schema is None or schema == "":
        return ""
    validated_schema = []
    to_be_validated = [s.strip() for s in schema.split(",")]
    for name in known_schema_names:
        if name in to_be_validated:
            validated_schema.append(name)
            to_be_validated.remove(name)
    if len(to_be_validated) != 0:
        raise ValueError(f"Unkown schema module name(s): {to_be_validated}")
    return ",".join(validated_schema)


# todo: improve this function
# also see _add_storage.validate_root_arg which errors
# upon non gs non-s3
def validate_storage_arg(storage: str) -> None:
    # google cloud or AWS
    # for instances that are stored on the hub,
    # this is a requirement
    if storage.startswith(("gs://", "s3://")):
        return None
    else:
        try:
            # try creating a path
            _ = Path(storage)
            return None
        except Exception:
            raise ValueError(
                "`storage` is neither a valid local, a Google Cloud nor an S3 path."
            )


def validate_db_arg(db: Optional[str]) -> None:
    if db is not None:
        if not db.startswith("postgresql"):
            raise ValueError("Only postgres connection strings are allowed.")


def validate_unique_sqlite(
    *, hub, db: Optional[str], storage_id: UUID, name: str, account: Mapping
) -> None:
    # if a remote sqlite instance, make sure there is no other instance
    # that has the same name and storage location
    if db is None:  # remote sqlite instance
        data = (
            hub.table("instance")
            .select("*")
            .eq("storage_id", storage_id)
            .eq("name", name)
            .execute()
            .data
        )
        if len(data) > 0:
            raise RuntimeError(
                "There is already an sqlite instance with the same name and storage"
                f" location from account: {account['handle']}\nYou cannot have two"
                " sqlite instances with the same name and the same storage\nFix:"
                " Choose another name!"
            )
