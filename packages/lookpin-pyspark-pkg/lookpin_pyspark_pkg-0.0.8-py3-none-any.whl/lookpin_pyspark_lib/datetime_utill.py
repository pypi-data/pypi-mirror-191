import datetime

KST = datetime.timezone(datetime.timedelta(hours=9))


def get_kst_datetime_index(index_name):
    return index_name + datetime.datetime.now(KST).strftime('%Y-%m-%d')


def get_utc_date_time_now():
    return datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0).strftime(
        '%Y-%m-%d %H:%M:%S')


def get_datetime_now_utc_replace_previous_days(days):
    return (datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0,
                                                                 microsecond=0) - datetime.timedelta(
        days=days)).strftime('%Y-%m-%d %H:%M:%S')
