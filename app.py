import os
import sqlite3
import datetime

from flask import Flask, render_template, request, redirect

from ai_engine import ask_ai
from database import init_db


# ---------------- INIT DATABASE ----------------

init_db()


# ---------------- APP SETUP ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


# ---------------- DATABASE ----------------

def get_db():
    return sqlite3.connect("arc.db")


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("stranger.html")


# ---------------- LEARNING ----------------

@app.route("/learn", methods=["GET", "POST"])
def learn():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        topic = request.form["topic"]
        status = request.form["status"]
        note = request.form["note"]

        today = str(datetime.date.today())

        cur.execute("""
        INSERT INTO learning (topic, status, note, date)
        VALUES (?, ?, ?, ?)
        """, (topic, status, note, today))

        conn.commit()
        conn.close()

        return redirect("/learn")


    cur.execute("""
    SELECT topic, status, note, date
    FROM learning
    ORDER BY id DESC
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("learn.html", data=data)


# ---------------- AI ----------------

@app.route("/ai", methods=["GET", "POST"])
def ai():

    answer = ""

    if request.method == "POST":

        q = request.form["question"]
        answer = ask_ai(q)

    return render_template("ai.html", answer=answer)


# ---------------- GAME LOGIN ----------------

@app.route("/game", methods=["GET", "POST"])
def game_login():

    if request.method == "POST":

        username = request.form["username"]

        return redirect(f"/play/{username}")

    return render_template("game_login.html")


# ---------------- PLAY GAME ----------------

@app.route("/play/<username>")
def play(username):

    return render_template("game.html", username=username)


# ---------------- SAVE SCORE ----------------

@app.route("/save_score", methods=["POST"])
def save_score():

    username = request.form.get("username")
    score = request.form.get("score")

    if not username or not score:
        return "Invalid Data", 400


    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO scores (username, score, date)
    VALUES (?, ?, date('now'))
    """, (username, score))

    conn.commit()
    conn.close()

    return "Saved"


# ---------------- LEADERBOARD (TOP 3) ----------------

@app.route("/leaderboard")
def leaderboard():

    conn = get_db()
    cur = conn.cursor()

    # Top score per user → then top 3 users
    cur.execute("""
    SELECT username, MAX(score) AS best_score
    FROM scores
    GROUP BY username
    ORDER BY best_score DESC
    LIMIT 3
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("leaderboard.html", data=data)


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    print("ARC Learning System Running...")

    app.run(host="0.0.0.0", port=port)
