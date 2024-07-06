import pytest
from api_client import ApiClient

@pytest.fixture()
def api_client():
    return ApiClient()