import itertools

from flask import request

from web.models import UrlModel
from web.utils import decode


def get_count(obj, id):
    url = obj.get_by_id(id)
    return url.count


def get_base_by_short(obj, short):
    mod = obj.get_or_none(id=decode(short))
    if mod.url_details.model.get_ip(short) is None:
        mod.url_details.model.add_ip(short, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
        add_to_count(obj,short)
        return obj.get_or_none(id=decode(short))
    return obj.get_or_none(id=decode(short))


def add_to_count(obj, short):
    url = obj.get_by_id(short)
    url.count += 1
    url.save()


def get_top_10_count():
    data = {}

    for i in UrlModel.select().order_by(UrlModel.count.desc()):
        data.update({f'url: {i.base_url}': f'count - {i.count}'})
    data_top = dict(itertools.islice(data.items(), 10))
    return data_top
