from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from application.forms import RegistrationForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_MYSQL_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
Session(app)
db = SQLAlchemy(app)

from application import routes

