import json, os

FILE = os.path.join(os.path.dirname(__file__), "profile.json")

def load_profile():
    if os.path.exists(FILE):
        with open(FILE,"r") as f:
            return json.load(f)
    return {}

def save_profile(profile):
    with open(FILE,"w") as f:
        json.dump(profile, f)
