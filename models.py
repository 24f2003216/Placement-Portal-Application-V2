from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)
    role = db.Column(db.String(50), nullable = False)

    is_active = db.Column(db.Boolean, default = True)
    is_approved = db.Column(db.Boolean, default = False)


    student_profile = db.relationship("Student", backref = "user", uselist = False, cascade = "all, delete-orphan")
    company_profile = db.relationship("Company", backref = "user", uselist = False, cascade = "all, delete-orphan")

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    name = db.Column(db.String(150), nullable = False)

    contact = db.Column(db.String(100))
    resume_filename = db.Column(db.String(255))
    
    applications = db.relationship('Application', backref = 'student', cascade = "all, delete-orphan")
 
class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    name = db.Column(db.String(150), nullable = False)

    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(255))

    drives = db.relationship('PlacementDrive', backref = 'company', cascade = "all, delete-orphan")

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable = False)
    job_title = db.Column(db.String(150), nullable = False)
    job_description = db.Column(db.Text, nullable = False)
    
    eligibility = db.Column(db.String(255), nullable = False)
    deadline = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String(50), default = 'Pending')

    applications = db.relationship('Application', backref = 'drive', cascade = "all, delete-orphan")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable = False)
    date_applied = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(50), default = 'Applied') 
