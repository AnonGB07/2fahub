import json

storage = {"credentials": [], "cookies": []}
config = {}
template_content = ""

def init_storage():
    storage["credentials"] = []
    storage["cookies"] = []

def load_template(template_path: str):
    global template_content
    with open(template_path, "r") as f:
        template_content = f.read()
