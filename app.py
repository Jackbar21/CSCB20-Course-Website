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

class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    assignment1 = db.Column(db.Float, nullable=False)
    assignment2 = db.Column(db.Float, nullable=False)
    assignment3 = db.Column(db.Float, nullable=False)
    tut_attendance = db.Column(db.Float, nullable=False)
    midterm = db.Column(db.Float, nullable=False)
    final = db.Column(db.Float, nullable=False)
    remark = db.relationship('Remark', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Instructor(db.Model):
    __tablename__ = 'Instructor'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    feedback = db.relationship('Feedback', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Remark(db.Model):
    __tablename__ = 'Remark'
    id = db.Column(db.Integer, primary_key=True)
    assessment = db.Column(db.String(100), nullable=False) # i.e. assignment1
    reason = db.Column(db.String(2500), nullable=False)
    status = db.Column(db.String(100), nullable=False) # Pending, Approved or Rejected
    student_id = db.Column(db.Integer, db.ForeignKey('Student.id'), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(2500), nullable=False)
    question2 = db.Column(db.String(2500), nullable=False)
    question3 = db.Column(db.String(2500), nullable=False)
    question4 = db.Column(db.String(2500), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.id'), nullable=False)

@app.route('/')
@app.route('/home')
def home():
    pagename = 'home'
    return render_template('home.html', pagename = pagename)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['Username']
        email = request.form['Email']
        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        user_type = request.form['User_Type']
        reg_details = (
            username,
            email,
            hashed_password,
            user_type
        )
        add_users(reg_details)
        flash('Registration Successful! Please login now:')
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            flash('already logged in!!')
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        username = request.form['Username']
        password = request.form['Password']
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = username
            #session['user_type'] = user.user_type
            session.permanent = True
            return redirect(url_for('home'))
        else:
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')

@app.route('/notes', methods = ['GET', 'POST'])
def notes():
    if request.method == 'GET':
        query_notes_result = query_notes()
        return render_template('notes.html', query_notes_result = query_notes_result)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        note_details = (
            request.form['Note_ID'],
            request.form['Title'],
            request.form['Content'],
            request.form['Your_ID']
        )
        add_notes(note_details)
        return render_template('add_success.html')

@app.route('/logout')
def logout():
    session.pop('user', default = None)
    #session.pop('user_type', default = None)
    return redirect(url_for('home'))

def query_notes():
    query_notes = Notes.query.all()
    return query_notes

def add_notes(note_details):
    note = Notes(
        id = note_details[0], 
        title = note_details[1], 
        content = note_details[2], 
        person_id = note_details[3]
        )
    db.session.add(note)
    db.session.commit()

def add_users(reg_details):
    user = User(
        username = reg_details[0],
        email = reg_details[1],
        password = reg_details[2],
        user_type = reg_details[3]
        )
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
