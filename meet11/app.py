from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'

db_user = "root"
db_password = ""
db_host = "localhost"
db_name = "meet11"

connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

@app.route("/", methods=["GET", "POST"])
def index():

    #insert data from form into db
    if request.method == "POST":
        note = request.form.get("note")
        try:
            cursor = connection.cursor()
            # cursor.execute(f"INSERT INTO notes (note) VALUES ('{note}');")
            cursor.execute("INSERT INTO notes (note) VALUES (%s);", note )
            connection.commit()
        finally:
            cursor.close()

    #read data all notes from db
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM notes;")
        notes = cursor.fetchall()
    except:
        notes = []
    finally:
        cursor.close()
    # print(notes)
    return render_template("index.html", notes=notes)

@app.route("/delete/<int:note_id>")
def delete(note_id):
    try :
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM notes WHERE id = {note_id}")
        note = cursor.fetchone()
        if note:
            cursor.execute(f"DELETE FROM notes WHERE id = {note_id}")
            connection.commit()
            msg = ("Your note had been already deleted.", "success")
        else:
            msg = ("Your note does not exists.", "warning")
    except:
        pass
    finally:
        cursor.close()
    flash(msg[0], msg[1])
    return redirect(url_for("index"))

@app.route("/update/<int:note_id>", methods=["GET", "POST"])
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
        cursor.execute(f"SELECT * FROM notes WHERE id = {note_id}")
        note = cursor.fetchone()
        # print(note)
    except:
        pass
    finally:
        cursor.close()

    return render_template("note_detail.html", note=note)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template()


@app.route("/logout")
def logout():
    pass




if __name__ == "__main__":
    app.run(debug=True)