import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_storage
from app.main import app
from app.storage import Storage


@pytest.fixture
def storage():
    return Storage()


@pytest.fixture
def client(storage):
    app.dependency_overrides[get_storage] = lambda: storage
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def user_headers():
    return {"X-User-Id": "10"}


@pytest.fixture
def admin_headers():
    return {"X-User-Id": "1", "X-User-Role": "admin"}
