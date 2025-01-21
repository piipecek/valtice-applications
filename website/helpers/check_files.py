import website.paths as p
import json
from website.logs import log

def check_data_folder() -> None:
    data_path = p.data_folder_path()
    if data_path.exists():
        log("data folder already exists")
    else:
        data_path.mkdir()
        log("creating data folder at " + str(data_path))


def check_logs_file() -> None:
    logs_path = p.log_file_path()
    if logs_path.exists():
        log("(this) log file already exists")
    else:
        logs_path.touch()
        log("creating (this) log file at  " + str(logs_path))
        

def check_settings_file() -> None:
    settings_path = p.settings_path()
    if settings_path.exists():
        log("settings file already exists")
    else:
        with open(settings_path, "w") as f:
            json.dump(
                {
                    "applications_start_date": "2025-01-01",
                    "applications_start_time": "00:00",
                    "applications_end_date": "2025-01-01",
                    "applications_end_time": "00:00",
                }
                , f)
        log("creating settings file at " + str(settings_path))

