import datetime
from website.paths import log_file_path

def log(data: str) -> None:
    with open(log_file_path(), "a") as file:
        file.write(str(datetime.datetime.utcnow()) + ":  " + data + "\n")

def get_app_logs() -> str:
    with open(log_file_path()) as file:
        return file.read()

def delete_app_logs() -> str:
    with open(log_file_path(), "w") as file:
        file.write("")

