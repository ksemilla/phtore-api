import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from resolvers.core import Query
from middlewares.authentication import BasicAuthBackend
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(
    schema,
)

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = FastAPI(middleware=middleware)
app.include_router(graphql_app, prefix="/graphql")
