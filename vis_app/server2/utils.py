

def replace(data):
    if data is not None:
        return data
    data = None
    return data


def generate(first,last):
    return first+last


def generate_otp(user_id, visitor_id):
    OTP = random.randint(1000, 9999);
    created = datetime.now();
    df = pd.DataFrame({'OTP': OTP, 'created': created, 'user_id': user_id,
                       'visitor_id': visitor_id}, index=[0])
    with dbm.dbManager() as manager:
        manager.commit(df, 'visitor_management_schema.opt')
        return OTP;

