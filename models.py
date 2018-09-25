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
    degree = db.StringField()
    area = db.StringField()
    institution = db.StringField()
    skill1 = db.StringField()
    skill2 = db.StringField()
    skill3 = db.StringField()
    skill4 = db.StringField()
    skill5 = db.StringField()
    skill6 = db.StringField()
    skill7 = db.StringField()
    skill8 = db.StringField()
    skill9 = db.StringField()


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
    solution = db.StringField()

class Scores(db.Document):
    applicant_id = db.StringField()
    job_id = db.StringField()
    applicant_solution = db.StringField()
    score = db.IntField()
    percentage_match = db.IntField()
    job_company = db.StringField()

class Applicants(db.Document):
    applicant_id = db.StringField()
    resume = db.StringField()
    percentage_match = db.StringField()
    job_id = db.StringField()
    filename = db.StringField()
