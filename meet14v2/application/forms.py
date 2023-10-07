from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4,max=8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Password must match")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4,max=8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Login")

class CreateNoteForm(FlaskForm):
    note = StringField("Note", validators=[Length(max=256)])
    submit = SubmitField("✅")

class UpdateNoteForm(FlaskForm):
    update_note = StringField("Update", validators=[DataRequired(), Length(max=256)])
    submit = SubmitField("✅")