from vis_app import create_app
app = create_app()
"""Create and return app."""
#app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
# load_blueprints(app)

#bcrypt = Bcrypt(app)
# app.run(debug=True)
# app.run()
