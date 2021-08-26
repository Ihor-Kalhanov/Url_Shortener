from web.utils import encode, decode


class TestUtils:

    def test_encode(self, url_model, app):
        test_encode_url = encode(url_model.id)

        assert isinstance(test_encode_url, str)

    def test_decode(self, url_model):
        test_decode_url = decode(str(url_model.id))

        assert isinstance(test_decode_url, int)


