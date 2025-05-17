from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import sys

sys.path.append("..")  # Подключаем родительскую папку для импорта

from utils import load_keys, encrypt_vote, save_vote, decrypt_candidate_totals
from voter_management import validate_token, has_already_voted, mark_voted
from zkp_pipeline import run_zkp_pipeline

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Кандидаты
CANDIDATES = {
    1: "Trump",
    2: "Obama",
    3: "Azat"
}

# Загрузка ключей
if not os.path.exists("../keypair/public.json"):
    from phe import paillier
    pub, priv = paillier.generate_paillier_keypair()
    from utils import save_keys
    save_keys(pub, priv)

public_key, private_key = load_keys()

@app.route("/", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        token = request.form.get("token")
        vote_str = request.form.get("vote")

        if not token or not vote_str:
            flash("❌ Пожалуйста, введите токен и выберите кандидата.", "error")
            return redirect(url_for("vote"))

        try:
            vote = int(vote_str)
        except ValueError:
            flash("❌ Неверный формат голоса.", "error")
            return redirect(url_for("vote"))

        voter = validate_token(token)
        if not voter:
            flash("❌ Неверный токен.", "error")
            return redirect(url_for("vote"))

        if has_already_voted(token):
            flash("⚠️ Вы уже проголосовали.", "warning")
            return redirect(url_for("vote"))

        if vote not in CANDIDATES:
            flash("❌ Неверный выбор кандидата.", "error")
            return redirect(url_for("vote"))

        if not run_zkp_pipeline(vote):
            flash("❌ Голос отклонён: ZKP-доказательство не пройдено.", "error")
            return redirect(url_for("vote"))

        enc_vote = encrypt_vote(public_key, vote)
        save_vote(enc_vote)
        mark_voted(token)
        flash("✅ Голос принят!", "success")
        return redirect(url_for("vote"))

    return render_template("vote.html", candidates=CANDIDATES)

@app.route("/results")
def results():
    from utils import load_votes
    votes = load_votes()
    if not votes:
        flash("Нет голосов для подсчета.", "info")
        return redirect(url_for("vote"))

    totals = decrypt_candidate_totals(private_key, votes, CANDIDATES)
    return render_template("results.html", results=totals, candidates=CANDIDATES)

if __name__ == "__main__":
    app.run(debug=True)
