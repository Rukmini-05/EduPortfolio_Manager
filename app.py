<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
=======
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Task
import os
>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rukmini@2005",
    database="student_management"
)

<<<<<<< HEAD
# ---------------- HOME ----------------
@app.route('/')
=======
# ---------------- LOGIN MANAGER ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- HOME ----------------
@app.route("/")
>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3
def home():
    return render_template("home.html") 



# ---------------- REGISTER ----------------
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

<<<<<<< HEAD
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
            (name, email, password)
        )
        db.commit()
        cursor.close()

=======
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3
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
<<<<<<< HEAD
            return "Invalid Login ❌"
=======
            flash("Invalid email or password")
>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
<<<<<<< HEAD
@app.route('/dashboard')
def dashboard():

    cursor = db.cursor(buffered=True, dictionary=True)
=======
@app.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tasks=tasks)


# ---------------- ADD TASK ----------------
@app.route("/add-task", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title")
>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3

    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

<<<<<<< HEAD
    cursor.execute("SELECT COUNT(*) AS total FROM tasks")
    total_tasks = cursor.fetchone()["total"]
=======
    return redirect(url_for("dashboard"))

>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3

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

<<<<<<< HEAD
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

=======
        new_student = Student(
            name=name,
            course=course,
            age=age,
            user_id=current_user.id   # link student to logged in user
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("students"))

    all_students = Student.query.filter_by(user_id=current_user.id).all()
    return render_template("students.html", students=all_students)
>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop("user", None)

    return redirect(url_for("home"))


<<<<<<< HEAD
# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
=======
# ---------------- RUN APP ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
>>>>>>> fe6f34eee4c6033dfb1f3b7a94b66e260ab933a3
