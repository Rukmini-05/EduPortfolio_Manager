from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rukmini@2005",
    database="student_management"
)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("home.html") 


# ---------------- REGISTER ----------------
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
            (name, email, password)
        )
        db.commit()
        cursor.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:
            session["user"] = user["name"]
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Login ❌"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    cursor = db.cursor(buffered=True, dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM tasks")
    total_tasks = cursor.fetchone()["total"]

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    cursor.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_tasks=total_tasks,
        tasks=tasks
    )


# ---------------- STUDENTS ----------------
@app.route('/students')
def students():

    if "user" not in session:
        return redirect(url_for("login"))

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()

    return render_template("students.html", students=students)


# ---------------- ADD STUDENT ----------------
@app.route('/add_student', methods=["POST"])
def add_student():

    name = request.form["name"]
    course = request.form["course"]
    age = request.form["age"]

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO students (name, course, age) VALUES (%s,%s,%s)",
        (name, course, age)
    )

    db.commit()
    cursor.close()

    return redirect(url_for("students"))


# ---------------- EDIT STUDENT ----------------
@app.route('/edit_student/<int:student_id>', methods=["GET", "POST"])
def edit_student(student_id):

    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        course = request.form["course"]
        age = request.form["age"]

        cursor.execute(
            "UPDATE students SET name=%s, course=%s, age=%s WHERE id=%s",
            (name, course, age, student_id)
        )

        db.commit()
        cursor.close()

        return redirect(url_for("students"))

    cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    student = cursor.fetchone()

    cursor.close()

    return render_template("edit_student.html", student=student)


# ---------------- DELETE STUDENT ----------------
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):

    cursor = db.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))

    db.commit()
    cursor.close()

    return redirect(url_for("students"))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop("user", None)

    return redirect(url_for("home"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)