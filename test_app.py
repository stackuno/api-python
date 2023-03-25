import pytest
from sanic_testing.testing import SanicASGITestClient

from app import api


@pytest.fixture
def app():
    return SanicASGITestClient(api)


@pytest.mark.asyncio
async def test_health_endpoint(app):
    request, response = await app.get("/healthz")
    assert request.method == "GET"
    assert response.status == 204
