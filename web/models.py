import peewee

from playhouse.db_url import connect
from flask import request

from web import utils

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
    def add_url(cls, url):
        return cls.get_url(url) or cls.create(base_url=url, count=0)

    @classmethod
    def get_base_by_short(cls, short):
        mod = cls.get_or_none(id=utils.decode(short))

        if mod.url_details.model.get_url(cls.get_or_none(id=utils.decode(short)).id) is None:
            mod.url_details.model.add_ip(cls.get_or_none(id=utils.decode(short)).id,
                                         request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            cls.add_to_count(cls.get_or_none(id=utils.decode(short)).id)
            return cls.get_or_none(id=utils.decode(short))

        return cls.get_or_none(id=utils.decode(short))

    @classmethod
    def add_to_count(cls, short):
        url = cls.get_by_id(short)
        url.count += 1
        url.save()



class IPModel(BaseUrlModel):
    url = peewee.ForeignKeyField(UrlModel, related_name='url_details')
    ip = peewee.CharField()

    @classmethod
    def get_url(cls, url):
        return cls.get_or_none(url=url)

    @classmethod
    def add_ip(cls, url, ip):
        return cls.get_url(url) or cls.create(url=url, ip=ip)
