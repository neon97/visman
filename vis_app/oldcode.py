#@user.route('/user/login', methods=['GET', 'POST'])
def login():
    logging.info("Running Login")
    validate_query = queries['user_login']

    username = request.form['username']
    password = request.form['password']
    user_login_query = validate_query.format(username, password)

    with dbm.dbManager() as manager:
            result = manager.getDataFrame(user_login_query)
            return jsonify(result.to_dict(orient='records'))
