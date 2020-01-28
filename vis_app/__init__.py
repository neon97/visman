from flask import Flask
from flask_bcrypt import Bcrypt

#from peewee import PostgresqlDatabase

from flask_bcrypt import Bcrypt

def create_app(config=None):
    """Create and return app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    load_blueprints(app)

    
    # db = PostgresqlDatabase(config.DATABASE_CONFIG['database'],
    #                     user=config.DATABASE_CONFIG['user'],
    #                     password=config.DATABASE_CONFIG['password'],
    #                     host=config.DATABASE_CONFIG['host'],
    #                     port=config.DATABASE_CONFIG['port'])
    return app


def load_blueprints(app):
    from vis_app.routes.server import server
    from vis_app.routes.user import user
    from vis_app.routes.flat import flat
    from vis_app.routes.society import society
    from vis_app.routes.visitor import visitor
    from vis_app.routes.dashboard import dashboard

    app.register_blueprint(server)
    app.register_blueprint(user)
    app.register_blueprint(society)
    app.register_blueprint(visitor)
    app.register_blueprint(flat)
    app.register_blueprint(dashboard)
