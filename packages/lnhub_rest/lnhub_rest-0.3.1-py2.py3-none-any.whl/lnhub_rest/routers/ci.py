from fastapi import APIRouter

from lnhub_rest._clean_ci import delete_ci_accounts, delete_ci_auth_users

router = APIRouter(prefix="/ci")


@router.delete("/users")
def delete_ci_users():
    delete_ci_accounts()
    delete_ci_auth_users()
