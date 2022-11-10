import strawberry

from database.users import UserManager

@strawberry.field
def run_script() -> str:
    UserManager.update_many({}, { "role": "user" })
    return ""