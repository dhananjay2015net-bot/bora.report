from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"
DB = "data.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        center TEXT NOT NULL,
        name TEXT NOT NULL,
        value TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )""")
    if conn.execute("SELECT COUNT(*) FROM admins").fetchone()[0] == 0:
        conn.execute("INSERT INTO admins(username, password_hash) VALUES (?, ?)",
                     ("admin", generate_password_hash("admin123")))
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.route("/", methods=["GET", "POST"])
def entry():
    centers = ["Center 1", "Center 2", "Center 3", "Center 4"]
    if request.method == "POST":
        center = request.form.get("center", "")
        name = request.form.get("name", "").strip()
        value = request.form.get("value", "").strip()
        if center not in centers or not name or not value:
            flash("सभी जानकारी भरना जरूरी है।", "error")
        else:
            conn = get_db()
            conn.execute("INSERT INTO entries(center, name, value) VALUES (?, ?, ?)",
                         (center, name, value))
            conn.commit()
            conn.close()
            flash("Entry सफलतापूर्वक सेव हो गई।", "success")
            return redirect(url_for("entry"))
    return render_template("entry.html", centers=centers)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = get_db()
        admin = conn.execute("SELECT * FROM admins WHERE username=?", (username,)).fetchone()
        conn.close()
        if admin and check_password_hash(admin["password_hash"], password):
            session["admin"] = username
            return redirect(url_for("dashboard"))
        flash("गलत Login ID या Password", "error")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    center = request.args.get("center", "All")
    conn = get_db()
    if center == "All":
        rows = conn.execute("SELECT * FROM entries ORDER BY id DESC").fetchall()
    else:
        rows = conn.execute("SELECT * FROM entries WHERE center=? ORDER BY id DESC",
                             (center,)).fetchall()
    conn.close()
    return render_template("dashboard.html", rows=rows, center=center)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
