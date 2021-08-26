import os
import pytest

from web.app import create_app
from web.models import UrlModel, IPModel, db


@pytest.fixture(scope='module')
def app():
    app = create_app()
    yield app
    db.drop_tables([UrlModel, IPModel])


@pytest.fixture
def url_model():
    url = 'https://conftest.com/conftest/'
    return UrlModel.add_url(url)
