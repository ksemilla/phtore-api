from strawberry.tools import create_type

from .users import (
    user,
    users,
    update_user,
    create_user,
    delete_user
)

from .auth import (
    login
)

Query = create_type(
    'Query',
    [
        user,
        users,
        update_user,
        create_user,
        delete_user,

        login,
    ]
)