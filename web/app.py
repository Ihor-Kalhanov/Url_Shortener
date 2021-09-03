from flask import Flask, redirect, render_template
from flask_restful import Api
from webargs.flaskparser import parser, abort
from flasgger import Swagger

from web.models import UrlModel, IPModel, db
from web.resources.short import ShortUrl, CountUrl


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config['SWAGGER'] = {
        'title': 'Shortener API',
        'uiversion': 3,
        'description': ''
    }
    swagger = Swagger(app)

    db.create_tables([UrlModel, IPModel], safe=True)

    @parser.error_handler
    def handle_request_parsing_error(err, req, schema):
        abort(422, errors=err.messages)

    @app.route('/api')
    def api_reference():
        return render_template('api.html')

    @app.route('/<short>')
    def do_redirect(short):
        url = UrlModel.get_base_by_short(short)
        if url:
            return redirect(url.base_url, code=302)
        abort(404)

    @app.errorhandler(404)
    def return_404(error):
        return render_template('404_error.html'), 404

    @app.route('/')
    def index():
        return render_template('index.html')

    api.add_resource(ShortUrl, '/short')
    api.add_resource(CountUrl, '/shortened_urls_count')

    return app


