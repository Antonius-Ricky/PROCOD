import pymysql
from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_session import Session
from functools import wraps
from forms import RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_user = os.getenv("DATABASE_USER")
db_password = os.getenv("DATABASE_PASSWORD")
db_host = os.getenv("DATABASE_HOST")
db_name = os.getenv("DATABASE_NAME")

connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

def protected_route(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper
    

@app.route("/", methods=["GET", "POST"])
@protected_route
def index():

    if request.method == "POST":
        note = request.form.get("note")

        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO notes (note) VALUES ('{note}');")
            connection.commit()
        finally:
            cursor.close()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM notes;")
        notes = cursor.fetchall()
    except:
        notes = []       
    finally:
        cursor.close()

    return render_template("index.html", notes=notes)

@app.route("/delete/<int:note_id>")
@protected_route
def delete(note_id):

    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM notes WHERE id = {note_id}")
        note = cursor.fetchone()

        if note:
            cursor.execute(f"DELETE FROM notes WHERE id = {note_id}")
            connection.commit()
            msg = ("Your note had been already deleted.", "success")

        else:
            msg = ("Your note does not exist.", "warning")

    except:
        pass 

    finally:
        cursor.close()

    flash(msg[0], msg[1])
    return redirect(url_for("index"))

@app.route("/update/<int:note_id>" , methods=["GET", "POST"])
@protected_route
def update(note_id):

    cursor = connection.cursor()
    if request.method == "POST":
        new_note = request.form.get("new_note")
        print(new_note, note_id)
        # cursor.execute(f"UPDATE notes SET note = {new_note} WHERE id = {note_id}")
        cursor.execute("UPDATE notes SET note = %s WHERE id = %s", (new_note, note_id))
        cursor.close()
        return redirect(url_for("index"))

    try:
        cursor.execute(f"SElECT * FROM notes WHERE id = {note_id}")
        note = cursor.fetchone()
        
    except:
        pass

    finally:
        cursor.close()

    return render_template("note_detail.html", note=note)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="POST":
        cursor = connection.cursor()
        username = request.form.get("username")
        password = request.form.get("password")

        cursor.execute("SELECT * FROM users WHERE username = %s", username)
        user = cursor.fetchone()
        if user:

            # if username == user[1] and password == user[2]:
            if username == user[1] and check_password_hash(user[2], password):
                # print("ok")
                session["user_id"] = user[0]
                flash("Login Successful", "success")
                return redirect(url_for("index"))
            else:
                flash("Wrong username or password!", "warning")
                # print("nok")
        else:
            flash("Wrong username or password!", "warning")
            # print("nothing")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit(): # handling form post
        # print(form.username.data, form.password.data)
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        cursor = connection.cursor()
        username = request.form.get("username")
        password = request.form.get("password")

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        flash("Registration Success", "success")
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route("/logout")
@protected_route
def logout():
    
    session.pop("user_id", None)
    flash("You have been logged out", "success")
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)