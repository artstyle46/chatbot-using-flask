from flask import Flask

def create_app():
    #Creating new App
    app = Flask(__name__)
    # Adding routes
    from .routes import routes
    app.register_blueprint(routes, url_prefix="/")

    return app
