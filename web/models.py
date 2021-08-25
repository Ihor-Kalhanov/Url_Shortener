import peewee
import itertools
from flask import request
from playhouse.db_url import connect

from web.utils import decode

db = connect('sqlite:///data.db')


class BaseUrlModel(peewee.Model):
    class Meta:
        database = db


class UrlModel(BaseUrlModel):
    base_url = peewee.TextField(unique=True)
    count = peewee.IntegerField()

    @classmethod
    def get_url(cls, url):
        return cls.get_or_none(base_url=url)

    @classmethod
    def get_count(cls, id):
        url = cls.get_by_id(id)
        return url.count

    @classmethod
    def get_base_by_short(cls, short):
        mod = cls.get_or_none(id=decode(short))
        if mod.url_details.model.get_ip(short) is None:
            mod.url_details.model.add_ip(short, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            cls.add_to_count(short)
            return cls.get_or_none(id=decode(short))
        return cls.get_or_none(id=decode(short))

    @classmethod
    def add_to_count(cls, short):
        url = cls.get_by_id(short)
        url.count += 1
        url.save()

    @staticmethod
    def get_top_10_count():
        data = {}

        for i in UrlModel.select().order_by(UrlModel.count.desc()):
            data.update({f'url: {i.base_url}': f'count - {i.count}'})
        data_top = dict(itertools.islice(data.items(), 10))
        return data_top

    @classmethod
    def add_url(cls, url):
        return cls.get_url(url) or cls.create(base_url=url, count=0)


class IPModel(BaseUrlModel):
    url = peewee.ForeignKeyField(UrlModel, related_name='url_details')
    ip = peewee.CharField()

    @classmethod
    def get_ip(cls, ip):
        return cls.get_or_none(url=ip)

    @classmethod
    def add_ip(cls, url, ip):
        return cls.get_ip(url) or cls.create(url=url, ip=ip)


db.create_tables([UrlModel, IPModel], safe=True)

