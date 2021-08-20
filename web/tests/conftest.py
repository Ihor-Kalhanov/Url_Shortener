import pytest


@pytest.fixture
def app():
    from web.app import app as flask_app
    yield flask_app
