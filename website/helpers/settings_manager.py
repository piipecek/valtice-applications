from website.paths import settings_path
import json
from datetime import datetime
from website.helpers.pretty_date import pretty_date

def get_settings() -> dict:
    with open(settings_path(), 'r') as f:
        return json.load(f)
    
def save_settings(settings: dict):
    with open(settings_path(), 'w') as f:
        json.dump(settings, f, indent=4)

def set_applications_start_date_and_time(date: str, time: str):
    settings = get_settings()
    settings['applications_start_date'] = date
    settings['applications_start_time'] = time
    save_settings(settings)

def set_applications_end_date_and_time(date: str, time: str):
    settings = get_settings()
    settings['applications_end_date'] = date
    settings['applications_end_time'] = time
    save_settings(settings)

def get_faze_for_dashboard() -> str:
    settings = get_settings()
    start_datetime = datetime.strptime(f"{settings['applications_start_date']} {settings['applications_start_time']}", "%Y-%m-%d %H:%M")
    end_datetime = datetime.strptime(f"{settings['applications_end_date']} {settings['applications_end_time']}", "%Y-%m-%d %H:%M")
    if datetime.now() < start_datetime:
        return "pred"
    elif datetime.now() > end_datetime:
        return "po"
    else:
        return "pri"

def get_datetime_zacatku_for_dashboard() -> str:
    settings = get_settings()
    return f"{pretty_date(settings['applications_start_date'])} v {settings['applications_start_time']}"