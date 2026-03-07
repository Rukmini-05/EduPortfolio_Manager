from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- INITIALIZE DATABASE ----------------
def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT,
        age INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        github_link TEXT,
        live_link TEXT
    )
    """)

    conn.commit()
    conn.close()


# Run database setup
init_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = user["name"]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Login ❌"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_tasks=total_tasks,
        tasks=tasks
    )


# ---------------- STUDENTS ----------------
@app.route("/students")
def students():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template("students.html", students=students)


# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["POST"])
def add_student():

    name = request.form["name"]
    course = request.form["course"]
    age = request.form["age"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name,course,age) VALUES (?,?,?)",
        (name, course, age)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("students"))


# ---------------- EDIT STUDENT ----------------
@app.route("/edit_student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        course = request.form["course"]
        age = request.form["age"]

        cursor.execute(
            "UPDATE students SET name=?, course=?, age=? WHERE id=?",
            (name, course, age, student_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)


# ---------------- DELETE STUDENT ----------------
@app.route("/delete_student/<int:student_id>")
def delete_student(student_id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("students"))


# ---------------- PROJECTS PAGE ----------------
@app.route("/projects")
def projects():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    conn.close()

    return render_template("projects.html", projects=projects)


# ---------------- ADD PROJECT ----------------
@app.route("/add_project", methods=["GET", "POST"])
def add_project():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        github_link = request.form["github_link"]
        live_link = request.form["live_link"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO projects (title,description,github_link,live_link) VALUES (?,?,?,?)",
            (title, description, github_link, live_link)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("projects"))

    return render_template("add_project.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect(url_for("home"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)