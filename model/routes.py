from test import app
from flask import jsonify


@app.route('/about', methods=['GET', 'POST'])
def about():
    return jsonify({'Company': 'Visitor Management',
                    'Dev center': 'Team Foundation',
                    'version': 'heroku test development'})


app.run()