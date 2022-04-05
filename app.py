from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    uid = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

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
    

@app.route("/user", methods=["GET", "POST"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["emailAddress"]
            session["email"] = email
            flash("Email was saved!", "info")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    
    flash("You are not logged in!", "info")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logged out successfully!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
