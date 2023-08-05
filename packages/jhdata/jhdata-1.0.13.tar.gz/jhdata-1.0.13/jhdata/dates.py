import datetime


class DateFormats:
    date_path = "%Y/%m/%d"
    date = "%Y-%m-%d"
    timestamp = "%Y%m%d_%H%M%S"


def archive_date_today():
    return datetime.datetime.today().strftime(DateFormats.date_path)


def current_date():
    return datetime.datetime.today().strftime(DateFormats.date)


def current_timestamp():
    return datetime.datetime.now().strftime(DateFormats.timestamp)


def backdated_timestamp(**kwargs):
    return (datetime.datetime.now() - datetime.timedelta(**kwargs)).strftime(DateFormats.timestamp)


def zero_timestamp():
    return datetime.datetime.fromtimestamp(0).strftime(DateFormats.timestamp)


def timestamp_to_epoch(timestamp):
    return int(datetime.datetime.strptime(timestamp, DateFormats.timestamp).timestamp())
