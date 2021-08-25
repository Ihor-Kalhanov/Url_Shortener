from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from validators import url
from webargs import fields, ValidationError
from webargs.flaskparser import use_kwargs

from web.utils import encode
from web.models import UrlModel, IPModel

parser = reqparse.RequestParser()


def validate_url(base_url):
    if not url(base_url):
        raise ValidationError("Invalid url")
    return True


class ShortUrl(Resource):
    args = {
        'base_url': fields.Str(required=True, validate=validate_url)
    }

    @staticmethod
    @use_kwargs(args)
    @swag_from('../docs/short.yaml')
    def post(base_url):
        base = request.url_root.replace('http://', '')
        short_url = encode(UrlModel.add_url(base_url).id)
        return {'result': base + short_url}


class CountUrl(Resource):
    args = {
        'url_count': fields.Str(validate=validate_url)
    }

    @swag_from('../docs/get_count.yaml')
    def get(self):

        data = UrlModel.get_top_10_count()
        return {'10 most popular urls': data}

    @staticmethod
    @use_kwargs(args)
    @swag_from('../docs/count.yaml')
    def post(url_count):
        short_url = encode(UrlModel.add_url(url_count).id)
        count = UrlModel.get_count(short_url)
        return {'count_url': count}
