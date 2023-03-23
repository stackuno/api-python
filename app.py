from sanic import Sanic
from sanic.response import empty, HTTPResponse
from sanic.request import Request
from sanic.log import logger

from sanic_ext import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody, Response

from uuid import UUID

from pydantic import Field
from pydantic.dataclasses import dataclass


import os

# TODO: Rename the service into something more descriptive
api = Sanic("service-python-template")

api.ext.openapi.describe(
    "Template API",
    description="This is just a demo, but is should *almost* provide all the answers!",
    version="0.1.0",  # because this is alpha
)

api.ext.openapi.add_security_scheme(
    "token", "http", scheme="bearer", bearer_format="JWT"
)


@dataclass
class ItemModel:
    id: str = Field(description="identifier of item", example="xyz123")
    name: str = "Something fun"


@api.post("/items")
@openapi.definition(
    body=RequestBody({"application/json": ItemModel}, required=True),
    response=[
        Response(
            {"application/json": ItemModel}, description="The created item", status=200
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
async def post_items(_: Request) -> HTTPResponse:
    """Item creation handler

    Creates the *item* and returns the created payload along with the generated
    id upon success.
    """
    return empty()


@api.get("/items/<item_id:uuid>")
@openapi.definition(
    response=Response(
        {
            "application/json": {
                "title": "Items",
                "type": "object",
                "properties": {
                    "object": {"title": "Object type", "type": "string"},
                    "url": {"title": "Canonical URL", "type": "string"},
                    "data": {
                        "title": "Data",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            }
        }
    ),
    tag="Items",
    secured={"token": []},
)
async def get_item(_: Request, item_id: UUID) -> HTTPResponse:
    logger.info(f"item_id: {item_id}")
    return empty()


@api.get("/healthz")
async def get_health(_: Request) -> HTTPResponse:
    # TODO: Implement real healthchecking
    logger.warning("Please do something serious here")
    return empty()


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
