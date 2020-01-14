from flask import Flask
from flask_bcrypt import Bcrypt

def create_app(config=None):
    """Create and return app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    load_blueprints(app)
    Bcrypt(app)
    return app


def load_blueprints(app):
    from vis_app.routes.server import server
    from vis_app.routes.user import user
    from vis_app.routes.flat import flat
    from vis_app.routes.society import society
    from vis_app.routes.visitor import visitor

    app.register_blueprint(server)
    app.register_blueprint(user)
    app.register_blueprint(society)
    app.register_blueprint(visitor)
    app.register_blueprint(flat)

