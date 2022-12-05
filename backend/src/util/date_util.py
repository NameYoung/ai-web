from datetime import datetime, timezone, timedelta


def format_date_to_iso8601(date):
    return date.isoformat(timespec='milliseconds')


def get_current_date_str():
    return format_date_to_iso8601(datetime.now())
