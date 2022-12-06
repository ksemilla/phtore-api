from strawberry.tools import create_type

from .utils import run_script

from .users import (
    user,
    users,
    update_user,
    create_user,
    delete_user
)

from .entity import (
    find_entity_by_slug,
    create_entity,
    entities,
    my_entities,
    entity,
    remove_banner,
)

from .auth import (
    login,
    verify_token,
)

from .datafeed import (
    upload,
    datafeed,
)

Query = create_type(
    'Query',
    [
        user,
        users,
        delete_user,

        find_entity_by_slug,
        entities,
        my_entities,
        entity,

        datafeed,

        run_script,
    ]
)

Mutation = create_type(
    'Mutation',
    [
        login,
        verify_token,

        create_user,
        update_user,

        create_entity,
        remove_banner,

        upload,
    ]
)