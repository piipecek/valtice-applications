from website.paths import settings_path
import json

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