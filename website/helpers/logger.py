from flask_login import current_user
from website.paths import logs_path
from datetime import datetime


def log(message: str) -> None:
    """
    Logs a message to the log file with a timestamp and user information.

    Args:
        message (str): The message to log.
    """
    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Get the current user's username
    username = current_user.get_full_name("cz")

    # Create the log message
    log_message = f"{timestamp} - {username}: {message}\n"

    # Write the log message to the log file
    with open(logs_path(), "a") as log_file:
        log_file.write(log_message)