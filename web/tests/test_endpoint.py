import json


class TestEndpoint:
    TEST_URL = 'https://test.com/test/'

    def test_index(self, client):
        res = client.get('/')
        assert res.status_code == 200

    def test_short(self, client):
        type = 'application/json'
        headers = {
            'Content-Type': type,
            'Accept': type
        }
        body = {
            "base_url": f'{self.TEST_URL}'
        }
        endpoint = 'http://0.0.0.0:5000/short'
        response = client.post(endpoint,
                               data=json.dumps(body),
                               headers=headers)

        assert response.status_code == 200
        assert response.content_type == type
        assert 'result' in json.dumps(response.json)

    def test_short_invalid(self, client):
        invalid_long_url = 'sptthg://test.com/test/'
        type = 'application/json'
        headers = {
            'Content-Type': type,
            'Accept': type
        }
        body = {
            "base_url": f'{invalid_long_url}'
        }
        endpoint = 'http://0.0.0.0:5000/short'
        response = client.post(endpoint,
                               data=json.dumps(body),
                               headers=headers)

        assert response.status_code == 422
        assert 'errors' in json.dumps(response.json)

