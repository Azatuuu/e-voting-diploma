import json

VOTERS_FILE = "voters.json"

def load_voters():
    with open(VOTERS_FILE) as f:
        return json.load(f)

def save_voters(voters):
    with open(VOTERS_FILE, "w") as f:
        json.dump(voters, f, indent=2)

def validate_token(token):
    voters = load_voters()
    for voter in voters:
        if voter["token"] == token:
            return voter
    return None

def has_already_voted(token):
    voter = validate_token(token)
    return voter["has_voted"] if voter else None

def mark_voted(token):
    voters = load_voters()
    for voter in voters:
        if voter["token"] == token:
            voter["has_voted"] = True
            break
    save_voters(voters)
