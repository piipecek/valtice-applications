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


def set_cz_frontpage_text(text: str):
    settings = get_settings()
    settings['cz_frontpage_text'] = text
    save_settings(settings)
    
    
def set_en_frontpage_text(text: str):
    settings = get_settings()
    settings['en_frontpage_text'] = text
    save_settings(settings)


def get_cz_frontpage_text() -> str:
    settings = get_settings()
    return settings['cz_frontpage_text']


def get_en_frontpage_text() -> str:
    settings = get_settings()
    return settings['en_frontpage_text']


def is_class_signup_allowed() -> bool:
    settings = get_settings()
    start_date = datetime.strptime(settings['applications_start_date'] + ' ' + settings['applications_start_time'], '%Y-%m-%d %H:%M')
    return datetime.now() > start_date