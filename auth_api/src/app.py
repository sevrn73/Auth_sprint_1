from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/hello-world')
    def hello_world():
        return 'Hello, World!'


    return app

def start_app():
    app = create_app()
    return app

if __name__ == '__main__':
    start_app()