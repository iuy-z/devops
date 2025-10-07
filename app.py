from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Initialize database (create table if not exists)
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        message TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, message FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=80)  # important for EC2
