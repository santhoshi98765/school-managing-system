from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_required, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/database_name'
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = login_manager(app)
login_manager.login_view = 'login'


# Define User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Define other database models
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(50))
    name = db.Column(db.String(50))
    semester = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref=db.backref('students', lazy=True))
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(12))
    address = db.Column(db.String(100))


# Routes
@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/studentdetails')
def student_details():
    students = Student.query.all() 
    return render_template('student_details.html', students=students)

# Other routes follow similarly

if __name__ == "__main__":
    app.run(debug=True)
