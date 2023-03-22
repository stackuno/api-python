from sanic import Sanic
from sanic.response import empty, HTTPResponse
from sanic.request import Request
from sanic.log import logger

import os

# TODO: Rename the service into something more descriptive
api = Sanic("service-python-template")


@api.get("/healthz")
async def get_health(_: Request) -> HTTPResponse:
    # TODO: Implement real healthchecking
    logger.warning("Please do something serious here")
    return empty()


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
