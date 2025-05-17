import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VOTERS_FILE = os.path.join(BASE_DIR, "voters.json")

def load_voters():
    with open(VOTERS_FILE, "r") as f:
        return json.load(f)

def validate_token(token):
    voters = load_voters()
    return token in voters

def has_already_voted(token):
    voters = load_voters()
    return voters.get(token, {}).get("voted", False)

def mark_voted(token):
    voters = load_voters()
    if token in voters:
        voters[token]["voted"] = True
        with open(VOTERS_FILE, "w") as f:
            json.dump(voters, f, indent=2)
