from flask import render_template, url_for
from application.utils import protected_route
from application import app
from application.forms import RegistrationForm, LoginForm, CreateNoteForm, UpdateNoteForm

@app.route("/", methods=["GET", "POST"])
@protected_route
def index():
    create_form = CreateNoteForm()

    return render_template('index.html', form=create_form)

@app.route("/delete/<int:note_id>")
@protected_route
def delete(note_id):
    pass

@app.route("/update/<int:note_id>" , methods=["GET", "POST"])
@protected_route
def update(note_id):
    update_form = UpdateNoteForm()

    return render_template('note_detail.html', form=update_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    return render_template('login.html', form=login_form)


@app.route("/register", methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()

    return render_template('signup.html', form=registration_form)

@app.route("/logout")
@protected_route
def logout():
    pass