from flask import Flask
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'axizoun'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://axizoun:axizoun123@ds213612.mlab.com:13612/axizoun'

db = MongoAlchemy(app)

class Employee(db.Document):
    email = db.StringField()
    password = db.StringField()
    first_name =  db.StringField()
    last_name = db.StringField()
    resume = db.StringField()
    jobs_applied = db.ListField(db.IntField())

class Employer(db.Document):
    email = db.StringField()
    password = db.StringField()
    company_name = db.StringField()
    first_name =  db.StringField()
    last_name = db.StringField()
    contact_number = db.StringField()
    about_company = db.StringField()
    location = db.StringField()
    jobs_posted = db.ListField(db.IntField())

class Job(db.Document):
    company_name = db.StringField()
    vacancy = db.StringField()
    skill_1 = db.StringField()
    skill_2 = db.StringField()
    skill_3 = db.StringField()
    skill_4 = db.StringField()
    skill_5 = db.StringField()
    position = db.StringField()
    location = db.StringField()
    description = db.StringField()
    start_date = db.StringField()
    apply_date = db.StringField()
    duration = db.IntField()
    stipend = db.IntField()
    applicants = db.ListField(db.StringField())
    status = db.StringField()
    problem_statement = db.StringField()

class Scores(db.Document):
    employee = db.DocumentField(Employee)
    job = db.DocumentField(Job)
    company = db.StringField()
    score = db.IntField()

class Company(db.Document):
    name = db.StringField()
    description = db.StringField()
