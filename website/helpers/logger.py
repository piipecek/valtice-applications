from flask_login import current_user
from website.paths import logs_path
from datetime import datetime


def log(message: str) -> None:
    """
    Logs a message to the log file with a timestamp and current_user information.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    username = current_user.get_full_name("cz") if current_user.is_authenticated else "odhlášený uživatel"
    log_message = f"{timestamp} - {username}: {message}\n"

    with open(logs_path(), "a") as log_file:
        log_file.write(log_message)


def get_logs_for_browser() -> str:
    with open(logs_path(), "r") as log_file:
        logs = log_file.read()
    logs = logs.replace("\n", "<br>")
    return logs