from sanic import Sanic
from sanic.response import empty, HTTPResponse
from sanic.request import Request
from sanic.log import logger

from sanic_ext import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody, Response

# https://github.com/google/pytype/issues/1105
from pydantic import BaseModel, Field  # pytype: disable=import-error

import os

# TODO: Rename the service into something more descriptive
api = Sanic("service-python-template")


class ItemModel(BaseModel):
    id: str = Field(description="identifier of item", example="xyz123")
    name: str


@api.post("/items")
@openapi.definition(
    body=RequestBody({"application/json": ItemModel}, required=True),
    response=[
        Response(
            {"application/json": ItemModel}, description="The created item", status=200
        ),
    ],
)
async def post_items(_: Request) -> HTTPResponse:
    """Item creation handler

    Creates the *item* and returns the created payload along with the generated
    id upon success.
    """
    return empty()


@api.get("/items")
async def get_items(_: Request) -> HTTPResponse:
    return empty()


@api.get("/healthz")
async def get_health(_: Request) -> HTTPResponse:
    # TODO: Implement real healthchecking
    logger.warning("Please do something serious here")
    return empty()


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
