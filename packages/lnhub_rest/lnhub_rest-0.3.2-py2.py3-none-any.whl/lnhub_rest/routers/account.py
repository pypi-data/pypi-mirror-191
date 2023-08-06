from fastapi import APIRouter

from .utils import supabase_client

router = APIRouter(prefix="/account")


@router.get("/{id}")
def get_account_by_id(id: str):
    data = supabase_client.table("account").select("*").eq("id", id).execute().data
    return data[0] if len(data) > 0 else None


@router.get("/handle/{handle}")
def get_account_by_handle(handle: str):
    data = (
        supabase_client.table("account").select("*").eq("handle", handle).execute().data
    )
    return data[0] if len(data) > 0 else None


@router.get("/resources/owned/instances/{handle}")
def get_account_instances(handle: str):
    data = (
        supabase_client.table("account")
        .select(
            """instance!fk_instance_account_id_account(
            *, account!fk_instance_account_id_account(handle, id))""".replace(
                "\n", ""
            )
        )
        .eq("handle", handle)
        .execute()
        .data
    )
    return data[0]["instance"] if len(data) > 0 else []
