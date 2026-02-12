import os
import sqlite3
import datetime

from flask import Flask, render_template, request, redirect

from ai_engine import ask_ai
from database import init_db


# Init DB
init_db()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


# ---------- DB ----------

def get_db():
    return sqlite3.connect("arc.db")


# ---------- HOME ----------

@app.route("/")
def home():
    return render_template("stranger.html")


# ---------- LEARN ----------

@app.route("/learn", methods=["GET","POST"])
def learn():

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        topic = request.form["topic"]
        status = request.form["status"]
        note = request.form["note"]

        today = str(datetime.date.today())

        cur.execute("""
        INSERT INTO learning (topic,status,note,date)
        VALUES (?,?,?,?)
        """,(topic,status,note,today))

        conn.commit()
        conn.close()

        return redirect("/learn")


    cur.execute("""
    SELECT topic,status,note,date
    FROM learning
    ORDER BY id DESC
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("learn.html", data=data)


# ---------- AI ----------

@app.route("/ai", methods=["GET","POST"])
def ai():

    answer = ""

    if request.method=="POST":

        q = request.form["question"]
        answer = ask_ai(q)

    return render_template("ai.html", answer=answer)


# ---------- GAME ----------

@app.route("/game", methods=["GET","POST"])
def game_login():

    if request.method=="POST":

        username = request.form["username"]

        return redirect(f"/play/{username}")

    return render_template("game_login.html")


@app.route("/play/<username>")
def play(username):

    return render_template("game.html", username=username)


@app.route("/save_score", methods=["POST"])
def save_score():

    username = request.form["username"]
    score = request.form["score"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO scores (username,score,date)
    VALUES (?,?,date('now'))
    """,(username,score))

    conn.commit()
    conn.close()

    return "Saved"


@app.route("/leaderboard")
def leaderboard():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT username,score,date
    FROM scores
    ORDER BY score DESC
    LIMIT 10
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("leaderboard.html", data=data)


# ---------- RUN ----------

if __name__=="__main__":

    port = int(os.environ.get("PORT",10000))

    print("ARC Running...")

    app.run(host="0.0.0.0",port=port)
