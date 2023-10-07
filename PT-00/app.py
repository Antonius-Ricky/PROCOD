from flask import Flask, render_template, request, redirect, session, url_for, flash

from flask_session import Session

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 5 * 60
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "OfPT5tg6KXOaJ-fwm3tjzIijcroLuUvlc2WzUFGwcog"
Session(app)

users = [
    {"username": "admin", "password": "12345"}
]

def find_user(username):
    for user in users:
        if user["username"] == username:
            return user
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user") is None:
        return redirect(url_for("login"))
    
    if session.get("notes") is None:
        session["notes"] = []

    if request.method == "POST":
        note = request.form.get("note")
        # notes.append(note)
        return redirect(f"https://en.wikipedia.org/wiki/{note}")

    return render_template("search.html", notes=session["notes"])

@app.route("/search", methods = ["GET" , "POST"])
def search():
    if session.get("user") is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        query = request.form.get("query")
        return redirect(f"https://en.wikipedia.org/wiki/{query}")
    return render_template("search.html", title="Wikipedia")

@app.route("/login", methods=["GET", 'POST'])
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
    app.run(debug=True)