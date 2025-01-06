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

