from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():

    notes = ["One", "Two", "Three"]

    return render_template("index.html", notes=notes)

@app.route("/about")
def about():

    return render_template("about.html", title="about")

if __name__ == "__main__":
    app.run(debug=True)