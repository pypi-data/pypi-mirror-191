import datetime

sql_ts_format = '%Y-%m-%d %H:%M:%S.%f'

def get_sql_ts():
    return datetime.datetime.now().strftime(sql_ts_format)[:-3]
