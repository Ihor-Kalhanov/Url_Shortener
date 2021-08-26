import itertools

from flask import request

from web.models import UrlModel
from web.utils import decode


class UrlController(UrlModel):

    def get_count(self, id):
        url = self.get_by_id(id)
        return url.count

    def add_to_count(self, short):
        url = self.get_by_id(short)
        url.count += 1
        url.save()

    @staticmethod
    def get_top_10_count():
        data = {}

        for i in UrlModel.select().order_by(UrlModel.count.desc()).limit(10):
            data.update({f'url: {i.base_url}': f'count : {i.count}'})
        return data


def get_base_by_short(obj, short):
    mod = obj.get_or_none(id=decode(short))
    if mod.url_details.model.get_url(short) is None:
        mod.url_details.model.add_ip(short, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
        UrlController.add_to_count(UrlModel, short)
        return obj.get_or_none(id=decode(short))
    return obj.get_or_none(id=decode(short))
