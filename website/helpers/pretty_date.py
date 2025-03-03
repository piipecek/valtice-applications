from typing import Union
from datetime import datetime, date

def pretty_datetime(_date: Union[str, datetime]) -> str:
    if isinstance(_date, str):
        _date, time = _date.split(" ")
        year, month, day = _date.split("-")
        time, milis = time.split(".")
        hour, minute, sec = time.split(":")
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