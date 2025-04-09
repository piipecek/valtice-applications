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


def set_primary_classes_start_date_and_time(date: str, time: str):
    settings = get_settings()
    settings['primary_classes_start_date'] = date
    settings['primary_classes_start_time'] = time
    save_settings(settings)
    

def set_secondary_classes_start_date_and_time(date: str, time: str):
    settings = get_settings()
    settings['secondary_classes_start_date'] = date
    settings['secondary_classes_start_time'] = time
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


def is_primary_class_signup_open() -> bool:
    settings = get_settings()
    primary_start_date = datetime.strptime(settings['primary_classes_start_date'] + ' ' + settings['primary_classes_start_time'], '%Y-%m-%d %H:%M')
    applications_end_date = datetime.strptime(settings['applications_end_date'] + ' ' + settings['applications_end_time'], '%Y-%m-%d %H:%M')
    return primary_start_date < datetime.now() < applications_end_date


def is_secondary_class_signup_open() -> bool:
    settings = get_settings()
    secondary_start_date = datetime.strptime(settings['secondary_classes_start_date'] + ' ' + settings['secondary_classes_start_time'], '%Y-%m-%d %H:%M')
    applications_end_date = datetime.strptime(settings['applications_end_date'] + ' ' + settings['applications_end_time'], '%Y-%m-%d %H:%M')
    return secondary_start_date < datetime.now() < applications_end_date


def is_class_signup_closed() -> bool:
    settings = get_settings()
    applications_end_date = datetime.strptime(settings['applications_end_date'] + ' ' + settings['applications_end_time'], '%Y-%m-%d %H:%M')
    return datetime.now() > applications_end_date
    

def get_user_lock_state() -> bool:
    settings = get_settings()
    return settings['users_locked']


def toggle_user_lock_state() -> bool:
    """returns the new state of the user lock"""
    settings = get_settings()
    settings['users_locked'] = not settings['users_locked']
    save_settings(settings)
    return settings['users_locked']

def set_both_capacities(vs, gym):
    settings = get_settings()
    settings['vs_capacity'] = vs
    settings['gym_capacity'] = gym
    save_settings(settings)
    
def set_bank_account(account: str):
    settings = get_settings()
    settings['bank_account'] = account
    save_settings(settings)