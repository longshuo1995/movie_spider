from flask import Flask


def create_app():
    app = Flask(__name__)
    return app


def register_blueprint(app):
    from app.web.wechat import web
    app.register_blueprint(web)
    from app.web.movie import web
    app.register_blueprint(web)
