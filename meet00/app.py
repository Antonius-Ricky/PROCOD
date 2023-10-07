from flask import Flask, render_template

from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():

    res = 4*10-5
    return str(res)

    return "Hello, flask!"
    
@app.route("/hello")
def hello():
    return "Hello, world!"

@app.route("/profile/<string:username>")
def profile(username):
    return render_template("profile.html", username=username)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return '<h1 color: "red"; font-weight: "bold">Welcome To My Page!</h1>'

@app.route("/isitnewyear")
def isitnewyear():
    day = datetime.now().day
    month = datetime.now().month

    # if day == 1 and month == 1:
    #     msg = "Happy New Years!!!"

    # else:
    #     msg = "Wait A Little Longer..."
    # return render_template("newyear.html", msg=msg)

    return render_template("newyear.html")

if __name__ == "__main__":
    app.run(debug=True)