from sanic import Sanic
from sanic.response import empty, HTTPResponse
from sanic.request import Request
from sanic.log import logger

from sanic_ext import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody, Response

from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass as pydataclass

import os

# TODO: Rename the service into something more descriptive
api = Sanic("service-python-template")

APP_PROTO = os.getenv("PROTOCOL", "http")
APP_HOST = os.getenv("HOST", "localhost")
APP_PORT = int(os.getenv("PORT", 8000))
APP_PROXY_AUTH = os.getenv("PROXY_AUTH", "NONE")

api.ext.openapi.raw(
    {
        "servers": [
            {
                "url": f"{APP_PROTO}://{APP_HOST}:{APP_PORT}",
            }
        ],
    }
)

if APP_PROXY_AUTH == "JWT":
    api.ext.openapi.add_security_scheme(
        "token", "http", scheme="bearer", bearer_format="JWT"
    )


api.ext.openapi.describe(
    "Template API",
    description="This is just a demo, but is should *almost* provide all the answers!",
    version="0.1.0",  # because this is alpha
    terms="https://example.org/terms",
)

api.ext.openapi.contact(
    "Example API Ops",
    url="env.example.org",
    email="api@example.org",
)


class ItemData(BaseModel):
    name: str = Field(example="Something fun")


class ItemId(BaseModel):
    id: str = Field(description="identifier of item", example="xyz123")


class Item(ItemId, ItemData):
    pass


@pydataclass
class ItemList(BaseModel):
    has_more: bool
    members: list[Item]


api.ext.openapi.tag(
    name="Items",
    description="The base entity type that we deal with",
)


@api.post("/items")
@openapi.definition(
    body=RequestBody({"application/json": ItemData}, required=True),
    response=[
        Response(
            {"application/json": Item}, description="The created item", status=200
        ),
        Response(
            {
                "application/json": {
                    "title": "Error",
                    "type": "object",
                    "properties": {"message": {"title": "Message", "type": "string"}},
                }
            },
            description="The error response",
            status=400,
        ),
    ],
    tag="Items",
    secured={"token": []},
)
async def post_item(_: Request) -> HTTPResponse:
    """Item creation handler

    Creates the *item* and returns the created payload along with the generated
    id upon success.
    """
    return empty()


@api.get("/items/<item_id:uuid>")
@openapi.definition(
    response=Response({"application/json": openapi.Component(Item)}),
    tag="Items",
    secured={"token": []},
)
# TODO: Check compat between spec and implementation
async def get_item(_: Request, item_id: UUID) -> HTTPResponse:
    logger.info(f"item_id: {item_id}")
    return empty()


@api.get("/items/")
@openapi.definition(
    response=Response(
        {"application/json": openapi.Component(ItemList)}, description="List of items"
    ),
    tag="Items",
    secured={"token": []},
)
async def get_items(_: Request) -> HTTPResponse:
    return empty()


@api.get("/healthz")
async def get_health(_: Request) -> HTTPResponse:
    # TODO: Implement real healthchecking
    logger.warning("Please do something serious here")
    return empty()


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=APP_PORT)
