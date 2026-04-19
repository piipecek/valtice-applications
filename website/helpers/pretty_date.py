from typing import Union
from datetime import datetime, date

def pretty_datetime(_date: Union[str, datetime]) -> str:
    if isinstance(_date, str):
        _date, time = _date.split(" ")
        year, month, day = _date.split("-")
        time, milis = time.split(".") if "." in time else (time, "0")
        hour_minute_sec = time.split(":")
        if len(hour_minute_sec) == 2:
            hour, minute = hour_minute_sec
            sec = "00"
        else:
            hour, minute, sec = hour_minute_sec
        minute = minute.rjust(2, "0")
        sec = sec.rjust(2, "0")
        return f"{day}. {month}. {year}, {hour}:{minute}:{sec}"
    elif isinstance(_date, datetime):
        minute = str(_date.minute).rjust(2, "0")
        second = str(_date.second).rjust(2, "0")
        return f"{_date.day}. {_date.month}. {_date.year}, {_date.hour}:{minute}:{second}"
    elif isinstance(_date, date):
        return f"{_date.day}. {_date.month}. {_date.year}"

def pretty_date(_date: Union[str, date]) -> str:
    if isinstance(_date, str):
        year, month, day = _date.split("-")
        return f"{day}. {month}. {year}"
    elif isinstance(_date, date):
        return f"{_date.day}. {_date.month}. {_date.year}"