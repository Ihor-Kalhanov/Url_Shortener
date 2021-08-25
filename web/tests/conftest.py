import pytest

from web.app import app as flask_app
from web.models import UrlModel


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def url_model():
    url = 'https://conftest.com/conftest/'
    return UrlModel.add_url(url)