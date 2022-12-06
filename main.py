import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from resolvers.core import Query, Mutation
from middlewares.authentication import BasicAuthBackend
from fastapi.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(
    schema,
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],),
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend()),
]

app = FastAPI(middleware=middleware)
app.include_router(graphql_app, prefix="/graphql")
app.mount("/media", StaticFiles(directory="media"), name="media")
