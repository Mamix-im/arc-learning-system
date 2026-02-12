from ai_engine import ask_ai

from flask import Flask, render_template, request, redirect
import sqlite3
import datetime
import os
import subprocess


base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static")
)


@app.route("/ai", methods=["GET","POST"])
def ai():

    answer = ""

    if request.method == "POST":

        q = request.form["question"]
        answer = ask_ai(q)

    return render_template("ai.html", answer=answer)

@app.route("/dashboard")
def dashboard():

    subprocess.Popen(["python", "dashboard.py"])

    return "<h2>Dashboard Opened</h2><a href='/'>Back</a>"



# Database connect function
def get_db():
    return sqlite3.connect("arc.db")


@app.route("/", methods=["GET","POST"])
def learn():

    conn = get_db()
    cur = conn.cursor()

    # Jab form submit ho
    if request.method == "POST":

        topic = request.form["topic"]
        status = request.form["status"]
        note = request.form["note"]

        today = str(datetime.date.today())

        # Data insert
        cur.execute("""
        INSERT INTO learning (topic,status,note,date)
        VALUES (?,?,?,?)
        """, (topic,status,note,today))

        conn.commit()
        conn.close()

        return redirect("/")


    # Data read
    cur.execute("""
    SELECT topic,status,note,date
    FROM learning
    ORDER BY id DESC
    """)

    data = cur.fetchall()
    conn.close()

    return render_template("learn.html", data=data)


if __name__ == "__main__":
    print("ARC Learning System Running...")
    app.run(debug=True)
