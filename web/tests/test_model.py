
class TestModel:

    def test_field(self, url_model, app):
        assert url_model.base_url == 'https://conftest.com/conftest/'
        assert url_model.count == 0
        assert isinstance(url_model.count, int)