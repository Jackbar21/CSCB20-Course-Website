from flask import Flask, redirect, url_for, render_template, request, session, flash
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
        flash("Login Successful!", "info")
        return redirect(url_for("user"))

    
    if "user" in session:
        flash("Already logged in!", "info")
        return redirect(url_for("user"))
    
    return render_template("login.html")
    

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    
    flash("You are not logged in!", "info")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logged out successfully!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
