from typing import Union

from lnhub_rest._sbclient import connect_hub_with_auth


def delete_instance(
    *,
    owner: str,  # owner handle
    name: str,  # instance name
) -> Union[None, str]:
    try:
        hub = connect_hub_with_auth()

        # get account
        data = hub.table("account").select("*").eq("handle", owner).execute().data
        account = data[0]

        # get instance
        data = (
            hub.table("instance")
            .select("*")
            .eq("account_id", account["id"])
            .eq("name", name)
            .execute()
            .data
        )
        if len(data) == 0:
            return "instance-not-exists"

        instance = data[0]

        (
            hub.table("account_instance")
            .delete()
            .eq("instance_id", instance["id"])
            .execute()
            .data
        )

        data = hub.table("instance").delete().eq("id", instance["id"]).execute().data

        # TODO: delete storage if no other instances use it
        return None
    finally:
        hub.auth.sign_out()
