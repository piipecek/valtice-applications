from pathlib import Path

def hadej_slova_db_path() -> Path:
    return Path.cwd() / "data" / "hadej_slova.json"

def tomiem_result_path() -> Path:
    return Path.cwd() / "tomiem_ipsum" / "result.txt"

def log_file_path() -> Path:
    return Path.cwd() / "data" / "logs.txt"

def multilang_path() -> Path:
    return Path.cwd() / "data" / "multilang.json"

def cernabila_getword_path() -> Path:
    return Path.cwd() / "cernabila" / "db.json"

def dotenv_path() -> Path:
    return Path.cwd() / ".env"

def ikonky_folder_path() -> Path:
    return Path.cwd() / "website" / "static" / "img" / "ikonky"

def acga_kody_slova() -> Path:
    return Path.cwd() / "acga" / "db.json"

def acga_default_formular() -> Path:
    return Path.cwd() / "acga" / "default_formular.json"