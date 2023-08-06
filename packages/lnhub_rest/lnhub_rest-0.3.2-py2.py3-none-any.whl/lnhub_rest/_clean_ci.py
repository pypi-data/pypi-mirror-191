from datetime import datetime, timedelta

from lamin_logger import logger
from sqlalchemy import text

from lnhub_rest import engine
from lnhub_rest._sbclient import connect_hub_with_auth


def delete_ci_instances() -> None:
    hub = connect_hub_with_auth()
    try:
        # Delete instances created by the CI more than one hour ago
        instance_to_delete = (
            hub.table("instance")
            .select("id")
            .like("name", "lamin.ci.instance.%")
            .lt("created_at", datetime.now() - timedelta(hours=1))
            .execute()
            .data
        )

        for index, instance in enumerate(instance_to_delete):
            (
                hub.table("account_instance")
                .delete()
                .eq("instance_id", instance["id"])
                .execute()
                .data
            )
            (hub.table("instance").delete().eq("id", instance["id"]).execute().data)
        if len(instance_to_delete) > 0:
            logger.info(f"{index + 1} instances deleted")
    except Exception as exception:
        raise Exception(exception)
    finally:
        hub.auth.sign_out()


def delete_ci_auth_users():
    # Delete users in auth.user table created by the CI more than one hour ago
    query = f"""
    delete
    from auth.users
    where email like 'lamin.ci.user.%'
    and created_at < '{str(datetime.now() - timedelta(hours=1))}';
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()


def delete_ci_accounts() -> None:
    # Delete accounts created by the CI more than one hour ago
    query = f"""
    delete
    from account
    where handle like 'lamin.ci.user.%'
    and created_at < '{str(datetime.now() - timedelta(hours=1))}';
    """
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()
