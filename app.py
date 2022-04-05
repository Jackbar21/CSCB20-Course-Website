from datetime import datetime, timedelta
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text # textual queries
from secrets import token_hex

app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(16) # from secrets import
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 15)
# CHOOSE IF WANT TO KEEP! # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_instructor = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.email}', '{'Instructor' if self.is_instructor else 'Student'}')"

@app.route("/")
def home():
    return "Welcome to A3!"

if __name__ == '__main__':
    app.run(debug=True)
