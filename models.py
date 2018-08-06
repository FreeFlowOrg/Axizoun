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

class Employer(db.Document):
    email = db.StringField()
    password = db.StringField()
    company_name = db.StringField()
    first_name =  db.StringField()
    last_name = db.StringField()

class Jobs(db.Document):
    company_name = db.StringField()
    vacancy = db.StringField()
    languages = db.ListField(db.StringField())
    position = db.StringField()
    start_date = db.DateTimeField()
    apply_date = db.DateTimeField()
    stipend = db.IntField()
    applicants = db.ListField(db.StringField())
    status = db.StringField()
