from flask import Flask
from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

from db.db import init_db
from api.v1.api_v1_blueprint import app_v1_blueprint


SWAGGER_URL = '/docs/'
API_URL = '/static/swagger_config.yml'
swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

def create_app():
    app = Flask(__name__)


    app.register_blueprint(swagger_blueprint)
    app.register_blueprint(app_v1_blueprint, url_prefix='/v1')

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)


    return app

def start_app():
    app = create_app()
    init_db(app)
    return app

if __name__ == '__main__':
    start_app()