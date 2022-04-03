from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return "Welcome to A3!"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["name_KEY"]
        session["user"] = user
        return redirect(url_for("user"))

    
    if "user" in session:
        return redirect(url_for("user"))
    
    return render_template("login.html")
    

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
