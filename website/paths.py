from pathlib import Path

def log_file_path() -> Path:
    return Path.cwd() / "data" / "logs.txt"

def dotenv_path() -> Path:
    return Path.cwd() / ".env"

def ikonky_folder_path() -> Path:
    return Path.cwd() / "website" / "static" / "img" / "ikonky"

def data_folder_path() -> Path:
    return Path.cwd() / "data"

def settings_path() -> Path:
    return Path.cwd() / "data" / "settings.json"

def logo_cz_path() -> Path:
    return Path.cwd() / "website" / "static" / "img" / "logo_cz.png" 

def logo_en_path() -> Path:
    return Path.cwd() / "website" / "static" / "img" / "logo_en.png"