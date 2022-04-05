from flask import Flask, redirect, url_for, render_template, request, session, flash
from secrets import token_hex
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = token_hex(16) # from secrets import
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Welcome to A3!"

if __name__ == '__main__':
    app.run(debug=True)
