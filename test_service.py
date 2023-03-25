import pytest
from sanic_testing.testing import SanicASGITestClient

from service import api


@pytest.fixture
def service():
    return SanicASGITestClient(api)


@pytest.mark.asyncio
async def test_health_endpoint(service):
    request, response = await service.get("/healthz")
    assert request.method == "GET"
    assert response.status == 204
