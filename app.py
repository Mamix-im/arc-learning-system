import os
import sqlite3
import datetime

from flask import Flask, render_template, request, redirect

from ai_engine import ask_ai
from database import init_db


# Initialize Database
init_db()


# App Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


# ---------- Database Helper ----------

def get_db():
    return sqlite3.connect("arc.db")


# ---------- Routes ----------


# Home Page (Stranger Design)
@app.route("/")
def home():
    return render_template("stranger.html")


# Learning Page
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


# AI Page
@app.route("/ai", methods=["GET", "POST"])
def ai():

    answer = ""

    if request.method == "POST":

        q = request.form["question"]
        answer = ask_ai(q)

    return render_template("ai.html", answer=answer)



# ---------- Run Server ----------

if __name__ == "__main__":

    print("ARC Learning System Running...")

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port, debug=True)
