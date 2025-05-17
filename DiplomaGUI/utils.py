import os
import json
import base64
from datetime import datetime
from phe import paillier

# Абсолютный путь до родительской папки (Diploma)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KEY_DIR = os.path.join(BASE_DIR, "keypair")
VOTES_FILE = os.path.join(BASE_DIR, "votes.json")

PUB_KEY_FILE = os.path.join(KEY_DIR, "public.json")
PRIV_KEY_FILE = os.path.join(KEY_DIR, "private.json")

def save_keys(public_key, private_key):
    os.makedirs(KEY_DIR, exist_ok=True)
    with open(PUB_KEY_FILE, "w") as f:
        json.dump({"n": public_key.n}, f)
    with open(PRIV_KEY_FILE, "w") as f:
        json.dump({"p": private_key.p, "q": private_key.q}, f)

def load_keys():
    with open(PUB_KEY_FILE) as f:
        pub_data = json.load(f)
    with open(PRIV_KEY_FILE) as f:
        priv_data = json.load(f)
    public_key = paillier.PaillierPublicKey(pub_data['n'])
    private_key = paillier.PaillierPrivateKey(public_key, priv_data['p'], priv_data['q'])
    return public_key, private_key

def encrypt_vote(public_key, vote: int):
    enc = public_key.encrypt(vote)
    ciphertext_bytes = enc.ciphertext().to_bytes((enc.ciphertext().bit_length() + 7) // 8, byteorder="big")
    return json.dumps({
        "ciphertext": base64.b64encode(ciphertext_bytes).decode(),
        "exponent": enc.exponent
    })

def decrypt_candidate_totals(private_key, encrypted_votes, candidates):
    totals = {c: 0 for c in candidates}

    for enc_vote in encrypted_votes:
        ciphertext = int.from_bytes(base64.b64decode(enc_vote["ciphertext"]), byteorder="big")
        exponent = enc_vote["exponent"]
        encrypted_number = paillier.EncryptedNumber(private_key.public_key, ciphertext, exponent)
        vote = private_key.decrypt(encrypted_number)

        if vote in candidates:
            totals[vote] += 1

    return totals




def load_votes():
    with open(VOTES_FILE, "r") as f:
        return json.load(f)




def log_vote(token: str, zkp_passed: bool):
    log_path = "logs/vote_log.json"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    entry = {
        "token": token,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "zkp_passed": zkp_passed
    }

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def save_vote(enc_vote_json):
    if os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, "r") as f:
            votes = json.load(f)
    else:
        votes = []

    votes.append(json.loads(enc_vote_json))

    with open(VOTES_FILE, "w") as f:
        json.dump(votes, f, indent=2)
