from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from application import app, db
from application.utils import login_required
from application.forms import *
from application.models import *

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = User.query.get(session["user_id"])
    notes = user.notes
    return render_template("index.html", notes = notes)

@app.route("/delete/<int:note_id>")
@login_required
def delete(note_id):
    note = Note.query.filter(Note.id == note.id, Note.created_by == session["user.id"].first())

    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Your note has just been deleted.", "success")
    else:
        flash("Your note doesn't exists.", "warning")

@app.route("/update/<int:note_id>", methods=["GET", "POST"])
@login_required
def update(note_id):
    form = UpdateNoteForm()
    note = Note.query.filter(Note.id == note.id, Note.created_by == session["user.id"].first())

    if form.validate_on_submit():
        new_note = form.note.data
        note.note = new_note
        db.session.commit()
        flash("Note updated.", "success")
        return redirect(url_for("index"))

    return render_template("note_detail.html", note=note)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                session["user_id"] = user.id
                flash("Login Successful", "success")
                return redirect(url_for("index"))

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        hashed_password = generate_password_hash(form.password.data, method='sha256')

    
    return render_template("signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    flash("You have been logged out", "success")
    return redirect(url_for("login"))
