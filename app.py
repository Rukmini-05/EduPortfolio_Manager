from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Allow frontend (Netlify) to access backend
CORS(app)

DATABASE = "database.db"


# ----------- DATABASE INIT (ADDED) -----------
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    conn.close()

    if user:
        session["user"] = username
        return redirect("https://eduportfolio-manager-8.onrender.com/dashboard")
    else:
        return "Invalid username or password"


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_db_connection()

    total_students = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_tasks = conn.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    tasks = conn.execute(
        "SELECT * FROM projects"
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_tasks=total_tasks,
        tasks=tasks
    )


# ---------------- ADD PROJECT ----------------
@app.route("/add_project", methods=["POST"])
def add_project():

    if "user" not in session:
        return redirect(url_for("home"))

    title = request.form["title"]
    description = request.form["description"]

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO projects (title, description) VALUES (?, ?)",
        (title, description)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# ---------------- CREATE ADMIN USER ----------------
@app.route("/create_user")
def create_user():

    conn = get_db_connection()

    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )
        conn.commit()
        message = "Admin user created. Username: admin | Password: admin123"

    except sqlite3.IntegrityError:
        message = "Admin user already exists. Username: admin | Password: admin123"

    conn.close()

    return message

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# ----------- RUN APP -----------

init_db()   # (ADDED)

if __name__ == "__main__":
    app.run(debug=True)