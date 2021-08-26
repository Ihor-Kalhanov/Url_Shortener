import peewee

from playhouse.db_url import connect

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


class IPModel(BaseUrlModel):
    url = peewee.ForeignKeyField(UrlModel, related_name='url_details')
    ip = peewee.CharField()

    @classmethod
    def get_url(cls, url):
        return cls.get_or_none(url=url)

    @classmethod
    def add_ip(cls, url, ip):
        return cls.get_url(url) or cls.create(url=url, ip=ip)

