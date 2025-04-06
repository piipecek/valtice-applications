import website.paths as p
import json

def check_data_folder() -> None:
    data_path = p.data_folder_path()
    if data_path.exists():
        pass
    else:
        data_path.mkdir()
        

def check_settings_file() -> None:
    settings_path = p.settings_path()
    if settings_path.exists():
        pass
    else:
        with open(settings_path, "w") as f:
            json.dump(
                {
                    "primary_classes_start_date": "2025-01-01",
                    "primary_classes_start_time": "00:00",
                    "secondary_classes_start_date": "2025-01-01",
                    "secondary_classes_start_time": "00:00",
                    "applications_end_date": "2025-01-01",
                    "applications_end_time": "00:00",
                    "cz_frontpage_text": "Tento text je nutné upravit z admin sekce.",
                    "en_frontpage_text": "This text has to be edited from the admin section.",
                    "users_locked": False,
                    "vs_capacity": 0,
                    "gym_capacity": 0,
                    "bank_account": "000000000/0000",
                }
                , f, indent=4)
