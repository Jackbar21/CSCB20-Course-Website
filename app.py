from datetime import datetime, timedelta
from distutils.log import error
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text # textual queries
from secrets import token_hex

app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(16) # from secrets import
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
  


    #remark = db.relationship('Remark', backref='author', lazy=True)

    def __repr__(self):
        return f"Student('{self.username}', '{self.email}')"
    
class Instructor(db.Model):
    __tablename__ = 'Instructor'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # commenting this for now
   # feedback = db.relationship('Feedback', backref='author', lazy=True)

    def __repr__(self):
        return f"Instructor('{self.username}', '{self.email}')"

class Remark(db.Model):
    __tablename__ = 'Remark'
    id = db.Column(db.Integer, primary_key=True)
    assessment = db.Column(db.String(100), nullable=False) # i.e. assignment1
    reason = db.Column(db.String(2500), nullable=False)
    status = db.Column(db.String(100), nullable=False) # Pending, Approved or Rejected
    #new thing
    student_username = db.Column(db.String(2500), nullable=False)
    #commenting this rn
    #student_id = db.Column(db.Integer, db.ForeignKey('Student.id'), nullable=False)
  

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(2500), nullable=False)
    question2 = db.Column(db.String(2500), nullable=False)
    question3 = db.Column(db.String(2500), nullable=False)
    question4 = db.Column(db.String(2500), nullable=False)
   #new thing
    instructor_username = db.Column(db.String(2500), nullable=False)
    #commenting this rn
    
    #instructor_id = db.Column(db.Integer, db.ForeignKey('Instructor.id'), nullable=False)

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
        )

        # Notice bool(None) returns False and bool(<class object>) returns True
        username_already_exists = bool(Student.query.filter_by(username = username).first()) or bool(Instructor.query.filter_by(username = username).first())
        email_already_exists = bool(Student.query.filter_by(email = email).first()) or bool(Instructor.query.filter_by(email = email).first())
        if username_already_exists:
            flash('This username already exists! Please try again.', 'error')
            return render_template('register.html')
        elif email_already_exists:
            flash('This email address already exists! Please try again.', 'error')
            return render_template('register.html')

        add_student(reg_details) if user_type == "student" else add_instructor(reg_details)
        
        flash('Registration Successful! Please login now:')
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            flash('You are already logged in!')
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        username = request.form['Username']
        password = request.form['Password']
        user_type = request.form['User_Type']

        if user_type == "student":
            user = Student.query.filter_by(username = username).first()
        else:
            user = Instructor.query.filter_by(username = username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = username
            session['user_type'] = user_type
            session.permanent = True
            return redirect(url_for('home'))
        else:
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')


""" adding app route for submitting Anon Feedback"""
@app.route('/Send_Anon_Feedback',methods = ['GET', 'POST'])
def Send_Anon_Feedback():
    pagename = 'Send_Anon_Feedback'
    #new stuff
    query_Instructor = Instructor.query.all()
    if request.method == 'GET':
        return render_template('Send_Anon_Feedback.html', pagename = pagename,query_Instructor=query_Instructor)
    elif request.method == "POST":
        question1 = request.form['Q1']
        question2 = request.form['Q2']
        question3 = request.form['Q3']
        question4 = request.form['Q4']
        instructor_username = request.form['Uname']
        feedback_details = (
            question1,
            question2,
            question3,
            question4,
            instructor_username
            )
        add_feedback(feedback_details)
        flash("Feedback submitted successfully!!")
        return render_template('Send_Anon_Feedback.html', pagename = pagename,query_Instructor=query_Instructor)

"""Adding app route for viewing Anon Feedback """
@app.route('/View_Anon_Feedback')
def View_Anon_Feedback():
    pagename = 'View_Anon_Feedback'
    query_Feedback_result = Feedback.query.all()
    
    return render_template('View_Anon_Feedback.html',pagename=pagename,query_Feedback_result=query_Feedback_result)
    
""" adding app route for View Grades as a student"""

@app.route('/View_Grades_Student',methods = ['GET', 'POST'])
def View_Grades_Student():
    pagename = 'View_Grades_Student'
    #new stuff
    query_Student_result = Student.query.order_by(Student.username)
    remark_query_result = Remark.query.all()
    #new Stuff
    if request.method == 'GET':
        return render_template('View_Grades_Student.html', pagename = pagename,query_Student_result= query_Student_result,remark_query_result=remark_query_result)

    elif request.method == 'POST':
        status = 'Pending'
        reason = request.form['Reason']
        assesment = request.form['Course_Work']
        student_username = request.form['Uname']
        remark_details = (
            assesment,
            reason,
            status,
            student_username
        )

        add_remark(remark_details)
        flash("You have succesfully submitted the re-mark request")
        return redirect(url_for('View_Grades_Student'))


#New route for Grades as an Instructor
@app.route('/View_Grades_Instructor')
def View_Grades_Instructor():
    pagename = 'View_Grades_Instructor'
    #new stuff
    query_Student_result = Student.query.order_by(Student.username)
    #new Stuff
    return render_template('View_Grades_Instructor.html', pagename = pagename,query_Student_result= query_Student_result)

# adding a new route for updating grades as an instructor


@app.route('/Update_Grades_Instructor/<int:id>',methods = ['GET', 'POST'])
def Update_Grades_Instructor(id):

    pagename = 'Update_Grades_Instructor'
    #new stuff
    Student_to_update = Student.query.get_or_404(id)
    
    if request.method == "POST":
        Student_to_update.assignment1 = request.form['A1']
        Student_to_update.assignment2 = request.form['A2']
        Student_to_update.assignment3 = request.form['A3']
        Student_to_update.tut_attendance = request.form['Att']
        Student_to_update.midterm = request.form['Mid']
        Student_to_update.final = request.form['Final']
        try:
            db.session.commit()
            return redirect('/View_Grades_Instructor')
        except:
            flash('There was a problem updating the grade',"error")
            return redirect('/View_Grades_Instructor')
    else:
        return render_template('Update_Grades_Instructor.html', pagename = pagename,Student_to_update=Student_to_update)
    #new Stuff
     
"""Route for View_Remark_Reqs"""
@app.route('/View_Remark_Reqs')
def View_Remark_Reqs():
    pagename = 'View_Remark_Reqs'
    #new stuff
   
    remark_query_result = Remark.query.all()

    return render_template('View_Remark_Reqs.html', pagename = pagename,remark_query_result=remark_query_result)

@app.route('/Update_Remark/<int:id>',methods = ['GET', 'POST'])
def Update_Remark(id):
    pagename = 'Update_Remark'
    Remark_to_update = Remark.query.get_or_404(id)
   
    if request.method == "POST":
        Remark_to_update.status =request.form['Status']+':'+ 'instructor comments: '+request.form['Explanation']
        try:
            db.session.commit()
            return redirect('/View_Remark_Reqs')   
        except:
            flash('There was a problem updating the request',"error")
            return redirect('/View_Remark')
    elif request.method == "GET":
        return render_template('/Update_Remark.html',pagename=pagename,Remark_to_update=Remark_to_update)
        
   
    

@app.route('/logout')
def logout():
    session.pop('user', default = None)
    session.pop('user_type', default = None)
    return redirect(url_for('home'))



def add_student(reg_details):
    student = Student(
        username = reg_details[0],
        email = reg_details[1],
        password = reg_details[2],
        assignment1 = -1,
        assignment2 = -1,
        assignment3 = -1,
        tut_attendance = -1,
        midterm = -1,
        final = -1,
        )

    db.session.add(student)
    db.session.commit()

def add_instructor(reg_details):
    instructor = Instructor(
        username = reg_details[0],
        email = reg_details[1],
        password = reg_details[2]
        )

    db.session.add(instructor)
    db.session.commit()
#stuff for submitting anon feedback

def add_feedback(Feedback_details):
    feedback = Feedback (
        question1 = Feedback_details[0],
        question2 = Feedback_details[1],
        question3 = Feedback_details[2],
        question4 = Feedback_details[3],
        instructor_username = Feedback_details[4]

        )
    
    db.session.add(feedback)
    db.session.commit()

# print(Student.query.filter_by(username = "jackbar").first())
"""New function for adding Re-Mark Requests"""
def add_remark(Remark_details):
    remark = Remark (
        assessment = Remark_details[0],
        reason = Remark_details[1],
        status = Remark_details[2],
        student_username = Remark_details[3]

        )
    
    db.session.add(remark)
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
