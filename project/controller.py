from project import app, render_template

@app.route("/")
def index():
    return "warm welcome"

@app.route("/login")
def login():
    return render_template("login.html.j2")

@app.route("/notesof/<user>")
def notes(user):
    # find the user
    return render_template("notes.html.j2")
