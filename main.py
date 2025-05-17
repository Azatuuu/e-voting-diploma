# from phe import paillier
# from py_ecc.secp256k1 import secp256k1 as ec
# from py_ecc.optimized_bls12_381 import add, multiply, G1
# import random
#
#
# def generate_paillier_keys():
#     """
#     Generates a Paillier public-private key pair.
#     """
#     public_key, private_key = paillier.generate_paillier_keypair()
#     return public_key, private_key
#
#
# def encrypt_vote(vote: int, public_key):
#     """
#     Encrypts a single integer vote using the Paillier public key.
#     """
#     encrypted = public_key.encrypt(vote)
#     return encrypted
#
#
# def homomorphic_tally(encrypted_votes):
#     """
#     Homomorphically sums a list of Paillier-encrypted votes.
#     """
#     from functools import reduce
#     from operator import add
#     return reduce(add, encrypted_votes)
#
#
# def decrypt_tally(encrypted_tally, private_key):
#     """
#     Decrypt the final tally using the Paillier private key.
#     """
#     return private_key.decrypt(encrypted_tally)
#
#
# def generate_ec_proof(vote):
#     """
#     Generates a zero-knowledge proof using elliptic curve cryptography.
#     """
#     secret_scalar = random.randint(1, ec.N - 1)
#
#     commitment = multiply(G1, vote)  # Commit to vote on curve
#     proof = multiply(G1, secret_scalar)  # Randomized proof
#     return commitment, proof
#
#
# def verify_ec_proof(commitment, proof):
#     """
#     Verifies the zero-knowledge proof.
#     """
#     return isinstance(commitment, tuple) and isinstance(proof, tuple)
#
#
# def cast_vote(vote, pub_key):
#     """
#     Casts a vote by encrypting and generating a proof.
#     """
#     enc_v = encrypt_vote(vote, pub_key)
#     proof = generate_ec_proof(vote)
#     return enc_v, proof
#
#
# def verify_cast_vote(enc_vote, proof):
#     """
#     Verifies the proof of a valid vote.
#     """
#     return verify_ec_proof(*proof)
#
#
# if __name__ == "__main__":
#     # Generate keys
#     pub_key, priv_key = generate_paillier_keys()
#
#     # Collect votes
#     votes = [0, 1, 1, 0, 1]  # Example votes
#     encrypted_votes = []
#
#     for v in votes:
#         enc_v, proof_data = cast_vote(v, pub_key)
#         if verify_cast_vote(enc_v, proof_data):
#             encrypted_votes.append(enc_v)
#         else:
#             print("Invalid vote or invalid proof detected.")
#
#     # Homomorphic tally
#     encrypted_tally = homomorphic_tally(encrypted_votes)
#     final_count = decrypt_tally(encrypted_tally, priv_key)
#     print("Final Tally:", final_count)
#
#
#
#
# from phe import paillier
# from py_ecc.secp256k1 import secp256k1 as ec
# from py_ecc.optimized_bls12_381 import add, multiply, G1
# import random
# from functools import reduce
# from operator import add as add_op
#
#
# def generate_paillier_keys():
#     public_key, private_key = paillier.generate_paillier_keypair()
#     return public_key, private_key
#
#
# def encrypt_vote(vote: int, public_key):
#     if vote not in [0, 1]:
#         raise ValueError("Invalid vote. Only 0 or 1 is allowed.")
#     return public_key.encrypt(vote)
#
#
# def homomorphic_tally(encrypted_votes):
#     return reduce(add_op, encrypted_votes)
#
#
# def decrypt_tally(encrypted_tally, private_key):
#     return private_key.decrypt(encrypted_tally)
#
#
# def generate_ec_commitment(vote):
#     return multiply(G1, vote)
#
#
# def generate_dummy_proof(vote, commitment):
#     r = random.randint(1, ec.N - 1)
#     proof = multiply(G1, r)
#     return {
#         "commitment": commitment,
#         "proof": proof,
#         "r": r,
#         "vote": vote
#     }
#
#
# def verify_dummy_proof(proof_data):
#     vote = proof_data["vote"]
#     commitment = proof_data["commitment"]
#     proof = proof_data["proof"]
#
#     if vote not in [0, 1]:
#         return False
#     expected_commitment = multiply(G1, vote)
#     return commitment == expected_commitment and isinstance(proof, tuple)
#
#
# def cast_vote(vote, pub_key):
#     enc_v = encrypt_vote(vote, pub_key)
#     commitment = generate_ec_commitment(vote)
#     proof = generate_dummy_proof(vote, commitment)
#     return enc_v, proof
#
#
# def verify_cast_vote(enc_vote, proof):
#     return verify_dummy_proof(proof)
#
#
# if __name__ == "__main__":
#     pub_key, priv_key = generate_paillier_keys()
#     votes = [0, 1, 1, 0, 1, 2]  # '2' will be rejected
#     encrypted_votes = []
#
#     for v in votes:
#         try:
#             enc_v, proof_data = cast_vote(v, pub_key)
#             if verify_cast_vote(enc_v, proof_data):
#                 encrypted_votes.append(enc_v)
#             else:
#                 print(f"Invalid proof for vote: {v}")
#         except ValueError as e:
#             print(f"Vote rejected: {e}")
#
#     if encrypted_votes:
#         encrypted_tally = homomorphic_tally(encrypted_votes)
#         final_count = decrypt_tally(encrypted_tally, priv_key)
#         print("Final Tally:", final_count)
#     else:
#         print("No valid votes to count.")
#
#
#
#
#
#  # paillier_voting.py
# from phe import paillier
#
# # === Этап 1: Генерация ключей ===
# print("\n=== Генерация ключей Paillier ===")
# public_key, private_key = paillier.generate_paillier_keypair()
# print("Ключи сгенерированы.")
#
# # === Этап 2: Ввод голосов ===
# votes = []
# while True:
#     choice = input("\nВведите голос (0 или 1), или 'q' для выхода: ")
#     if choice.lower() == 'q':
#         break
#     if choice not in ['0', '1']:
#         print("Ошибка: введите 0 или 1")
#         continue
#     encrypted_vote = public_key.encrypt(int(choice))
#     votes.append(encrypted_vote)
#     print("Голос зашифрован и сохранён.")
#
# # === Этап 3: Подсчет голосов ===
# if not votes:
#     print("\nНет голосов для подсчета.")
# else:
#     total_encrypted = votes[0]
#     for v in votes[1:]:
#         total_encrypted += v
#     total = private_key.decrypt(total_encrypted)
#     print(f"\nВсего голосов '1': {total} из {len(votes)}")
from utils import load_keys, encrypt_vote, save_vote, save_keys, log_vote, decrypt_candidate_totals
from voter_management import validate_token, has_already_voted, mark_voted
from phe import paillier
import os

# Генерация ключей, если их нет
if not os.path.exists("keypair/public.json"):
    print("Генерируются ключи...")
    pub, priv = paillier.generate_paillier_keypair()
    save_keys(pub, priv)
else:
    print("Загрузка ключей...")

public_key, private_key = load_keys()

# Голосование
while True:
    print("\n--- Голосование ---")
    token = input("Введите ваш токен (или 'q' для выхода): ")
    if token.lower() == 'q':
        break

    voter = validate_token(token)
    if not voter:
        print("❌ Неверный токен.")
        continue

    if has_already_voted(token):
        print("⚠️ Вы уже проголосовали.")
        continue

    print("Кандидаты:")
    print("1 — Trump")
    print("2 — Obama")
    print("3 — Azat")

    vote = input("Введите ваш голос (1, 2 или 3): ")
    if vote not in ['1', '2', '3']:
        print("❌ Неверный ввод.")
        continue

    from zkp_pipeline import run_zkp_pipeline

    if run_zkp_pipeline(int(vote)):
        log_vote(token, True)
        enc_vote_json = encrypt_vote(public_key, int(vote))
        save_vote(enc_vote_json)
        mark_voted(token)
        print("✅ Голос принят!")
    else:
        log_vote(token, False)
        print("❌ Голос отклонён: доказательство не пройдено.")

# Подсчёт голосов по каждому кандидату
show_results = input("\nХотите подсчитать голоса? (y/n): ")
if show_results.lower() == 'y':
    from utils import load_votes, decrypt_candidate_totals, log_vote, decrypt_candidate_totals

    encrypted_votes = load_votes()
    if not encrypted_votes:
        print("Нет голосов.")
    else:
        candidates = {
            1: "Trump",
            2: "Obama",
            3: "Azat"
        }

        totals = decrypt_candidate_totals(private_key, encrypted_votes, list(candidates.keys()))

        print("\n📊 Результаты голосования:")
        for cid, name in candidates.items():
            print(f"{name}: {totals[cid]} голос(ов)")
