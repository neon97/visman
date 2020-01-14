from flask import Flask


def create_app(config=None):
    """Create and return app."""
    app = Flask(__name__)
    load_blueprints(app)
    return app


def load_blueprints(app):
    from vis_app.server1.routes import s1
    from vis_app.server2.server import server

    app.register_blueprint(s1)
    app.register_blueprint(server)

