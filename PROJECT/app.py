from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 5 * 60
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "OfPT5tg6KXOaJ-fwm3tjzIijcroLuUvlc2WzUFGwcog"
Session(app)

# notes = []

users = [
    {"username": "admin", "password": "12345"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user") is None:
        return redirect(url_for("login"))
    
    if session.get("notes") is None:
        session["notes"] = []

    if request.method == "POST":
        note = request.form.get("note")
        # notes.append(note)
        return redirect(f"en.wikipedia.org/wiki/Cat/{note}")

    return render_template("index.html", notes=session["notes"])

def find_user(username):
    for user in users:
        if user["username"] == username:
            return user
        return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if session.get("user") is not None:
            redirect(url_for("index"))

        user = find_user(username)
        if user:
            if user["password"] == password:
                session["user"] = user
                return redirect(url_for("index"))
        flash("Something went wrong!", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    if session.get("user"):
        session.pop("user")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)