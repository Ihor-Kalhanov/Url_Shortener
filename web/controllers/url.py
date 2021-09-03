from web.models import UrlModel


class UrlController(UrlModel):

    def get_count(self, id):
        url = self.get_by_id(id)
        return url.count

    @staticmethod
    def get_top_10_count():
        data = {}

        for i in UrlModel.select().order_by(UrlModel.count.desc()).limit(10):
            data.update({f'url: {i.base_url}': f'count : {i.count}'})
        return data
