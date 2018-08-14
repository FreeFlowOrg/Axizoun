#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask,flash,Blueprint,render_template,request,redirect,session,url_for,abort,send_file,safe_join
from flask_bootstrap import Bootstrap
from flask_mongoalchemy import MongoAlchemy
from flask_uploads import UploadSet,configure_uploads,DOCUMENTS
from models import *
import bcrypt
import logging
from logging import Formatter, FileHandler
import os
import boto3,botocore
from shutil import copyfile
import numpy
import difflib
import sys
import subprocess as s

from textanalyser.textanalyser import find

from photoanalysistool0.sliding_window_approach import info


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object('config')


files = UploadSet('files',DOCUMENTS)
app.config['UPLOADED_FILES_DEST'] = 'static/resumes'
app.config['UPLOADED_FILES_ALLOW']=['doc','docx','pdf','jpg','png']
configure_uploads(app,files)

s3 = boto3.client('s3')

@app.route('/')
def index():
    return render_template('forms/index.html')

### Authentication and Authorization
@app.route('/register/<type>', methods=['POST', 'GET'])
def register(type):
        # store hashed password and credentials for POST request
    if request.method == 'POST': # if data is being POSTed
        if type =='employee':
            employees = Employee.query.all()
            for employee in employees: # looping through the users
                if employee.email == request.form['email']: # check if the entered username matches to avoid collisions
                    flash('email already exists. Please pick another one')
                    return redirect(url_for('register',type='employee'))

                elif len(request.form['password'])<8: # password length check
                    flash('Please provide a password which is atleast 8 characters long')
                    return redirect(url_for('register',type='employee'))

                elif request.form['password'] != request.form['repeat_password']: # check passwords match
                    flash('Passwords mismatch. Please try again')
                    return redirect(url_for('register',type='employee'))
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10)) # hashing the password with a salt
            user_data = Employee(email = request.form['email'],password = hashed_password.decode('utf-8'),first_name = request.form['first_name'],last_name = request.form['last_name'],resume='',jobs_applied=[])# storing the hashed password in the collection
            user_data.save()
            flash('Signup Success!') # flash messages
            return redirect(url_for('index'))
    # if no exception, go here

        elif type == 'employer':
            employers = Employer.query.all()
            for employer in employers: # looping through the users

                if employer.email == request.form['email']: # check if the entered username matches to avoid collisions
                    flash('email already exists. Please pick another one')
                    return redirect(url_for('register',type='employer'))

                elif len(request.form['password']) < 8: # password length check
                    flash('Please provide a password which is atleast 8 characters long')
                    return redirect(url_for('register',type='employer'))

                elif request.form['password'] != request.form['repeat_password']: # check passwords match
                    flash('Passwords mismatch. Please try again')
                    return redirect(url_for('register',type='employer'))

            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10)) # hashing the password with a salt
            user_data = Employer(email = request.form['email'],password = hashed_password.decode('utf-8'),company_name = request.form['company_name'],first_name = request.form['first_name'],last_name = request.form['last_name'],contact_number=request.form['contact_number'],about_company=request.form['about_company'],location = request.form['location'] ,jobs_posted = []) # storing the hashed password in the collection
            user_data.save() # save
            flash('Signup Success!') # flash messages
            return redirect(url_for('index'))
    # render form for GET
    return render_template('forms/index.html')


@app.route('/login/<type>', methods=['POST'])
def login(type):
    if request.method == 'POST':
        if type == 'employee': #employee login
            employee = Employee.query.filter_by(email=request.form['email']).first()

            if employee is None:
                flash('No user has registered with this email')
                return redirect(url_for('index'))

            if bcrypt.hashpw(request.form['password'].encode('utf-8'),employee.password.encode('utf-8')) == employee.password.encode('utf-8'):
                session['email'] = request.form['email']
                session['user_type'] = type
                session['employee_id'] = str(employee.mongo_id)
                session['employee_resume'] = employee.resume
                return redirect(url_for('employee_dashboard'))
            else:
                flash('Wrong password entered. Please try again.')
                return redirect(url_for('index'))

        elif type == 'employer':

            employer = Employer.query.filter_by(email=request.form['email']).first()

            if employer is None:
                return redirect(url_for('index'))
                flash('No user registered with the specifed email')


            if bcrypt.hashpw(request.form['password'].encode('utf-8'),employer.password.encode('utf-8')) == employer.password.encode('utf-8'):
                session['email'] = request.form['email']
                session['user_type'] = type
                session['employer_id'] = str(employer.mongo_id)
                session['employer_company'] = employer.company_name
                return redirect(url_for('employer_dashboard'))

            else:
                flash('Incorrect Credentials Entered')
                return redirect(url_for('index'))

### employer routes

@app.route('/employee_dashboard')
def employee_dashboard():
    # provision for text extractor and profile maker
    employee = Employee.query.filter(Employee.mongo_id == session['employee_id']).first()
    if employee.resume == '':
        session['profile_submitted'] = 'unset'
        flash('Please submit your resume to apply for jobs')
    else:
        session['profile_submitted'] = 'set'
    return render_template('pages/profile_emp.html',employee=employee,profile_submitted=session['profile_submitted'])

@app.route('/employer_dashboard')
def employer_dashboard():
    employer = Employer.query.filter(Employee.mongo_id == session['employer_id']).first()
    jobs_posted = Job.query.filter(Job.company_name == employer.company_name ).all()
    return render_template('pages/profile_company.html',employer=employer,jobs=jobs_posted)

@app.route('/applicants/<job_id>')
def applicants(job_id):
    pass


### employee routes

@app.route('/post_jobs',methods=['POST','GET'])
def post_jobs():
    if request.method == 'GET':
        return render_template('pages/post_a_job.html')
    if request.method =='POST':
        job = Job(company_name = session['employer_company'],skill_1=request.form['skill_1'],skill_2=request.form['skill_2'],skill_3=request.form['skill_3']
        ,skill_4=request.form['skill_4'],skill_5=request.form['skill_5'],position=request.form['position'],location=request.form['location'],
        description=request.form['description'],start_date=request.form['start_date'],apply_date=request.form['apply_date'],duration=int(request.form['duration']),stipend=int(request.form['stipend']),applicants=[],status='vacant',problem_statement=request.form['problem_statement'])
        job.save()
        flash('Your job has been posted!')
        return redirect(url_for('employer_dashboard'))



@app.route('/resume_uploader',methods=['POST','GET'])
def resume_uploader():
    if request.method == 'POST' and 'file' in request.files:
        filename = files.save(request.files['file'])
        file = request.files['file']
        employee = Employee.query.filter(Employee.email == session['email']).first()
        employee.resume = filename
        employee.save()
        flash('Resume uploaded!')
        return redirect(url_for('employee_dashboard'))

@app.route('/skill_matcher_job_vacancies',methods=['POST','GET'])
def skill_matcher_job_vacancies():
    jobs = Job.query.all()
    vacancies = Job.query.filter(Job.status == 'vacant').all()

    perc = {}
    for job in jobs:
        file = open('job_desc.txt','w') #open a job_desc.txt
        file.write(job.description) #write job description to it
        file.close()# close the file
        os.mkdir('static/CV')# make a directory
        copyfile(os.path.join('static/resumes/',session['employee_resume']),os.path.join('static/CV/',session['employee_resume']))# copied file contents
        perc[job.description] = int((find('job_desc.txt','static/CV','textanalyser/model')[0][0])*100)
        os.remove(os.path.join('static/CV/',session['employee_resume']))
        os.rmdir('static/CV')
        os.remove('job_desc.txt')
        file = open('perc.txt','w')
        file.write(str(perc[job.description]))
        file.close()
    return render_template('pages/job_vacancies.html',jobs=vacancies,perc=perc)


# upload to local storage
@app.route('/upload_files/<job_id>/<employee_id>',methods=['POST','GET'])
def upload_files(job_id,employee_id):
    if request.method == 'POST' and 'answer' in request.files:
        filename = files.save(request.files['answer'])
        file = request.files['answer']
        resume = Employee.query.filter(Employee.mongo_id == session['employee_id']).first().resume
        applicant = Applicants(applicant_id = session['employee_id'],resume=resume,percentage_match = session['percentage_match'],job_id=session['job_id'],filename=filename)
        applicant.save()
        flash('You final submission has been received! You\'ll receive a confirmation mail if you\'ve been selected!')
        return redirect(url_for('photo_analysis',job_id=job_id,employee_id = employee_id))

@app.route('/photo_analysis/<job_id>/<employee_id>')
def photo_analysis(job_id,employee_id):
    filename = Applicants.query.filter(Applicants.job_id==job_id,Applicants.applicant_id==employee_id).first().filename
    employer_solution = Job.query.filter(Job.mongo_id == job_id).first().solution


    os.mkdir('static/employee_solutions') # create a directory for temporary assessment of applicant solutions
    os.mkdir('static/employer_solutions') # create a directory for employer solution

    s.call("python3 photoanalysistool0/sliding_window_approach/sliding_window.py -i "+os.path.join(app.config['UPLOADED_FILES_DEST'],filename), shell=True) # Run sliding window algorithm on applicant solution
    copyfile('extracted_info.txt','static/employee_solutions/employee_solution.txt') #copy into temporary directory
    file1 = 'static/employee_solutions/employee_solution.txt' #plug the path into a python variable
    os.remove('extracted_info.txt')

    s.call("python3 photoanalysistool0/sliding_window_approach/sliding_window.py -i "+os.path.join(app.config['UPLOADED_FILES_DEST'],employer_solution), shell=True) # Run sliding window algorithm on employer solution
    copyfile('extracted_info.txt','static/employer_solutions/employer_solution.txt') # copy into emploer sol dir
    file2 = 'static/employer_solutions/employer_solution.txt' #plug the path into a python variable

    with open(file1, 'r') as myfile:
         file1=myfile.read().replace('\n', '')

    with open(file2, 'r') as myfile:
         file2=myfile.read().replace('\n', '')

    perc = difflib.SequenceMatcher(None, file1, file2)

    print ('perc is %f' %(perc.ratio()*100)) # percentage difference between answers

    score = int(round(perc.ratio()*100,1))

    os.remove('extracted_info.txt')
    os.remove('static/employee_solutions/employee_solution.txt')
    os.rmdir('static/employee_solutions')
    os.remove('static/employer_solutions/employer_solution.txt')
    os.rmdir('static/employer_solutions')


    applicant = Applicants.query.filter(Applicants.job_id==job_id,Applicants.applicant_id==employee_id).first()
    score = Scores(applicant_id=employee_id,job_id=job_id,applicant_solution=applicant.filename,score=score)
    score.save()

    flash('Your solution has been successfully submitted. The results will be corressponded to you via mail.')

    return redirect(url_for('employee_dashboard'))


@app.route('/vacancies')
def vacancies():
    vacancies = Job.query.filter(Job.status == 'vacant').all()
    return render_template('pages/job_vacancies.html',jobs = vacancies,perc={})

@app.route('/applied_jobs')
def applied_jobs():
    employee = Employee.query.filter(Employee.mongo_id == session['employee_id']).first()
    applied_jobs = employee.jobs_applied
    return render_template('pages/appliedJobs.html',applied_jobs=applied_jobs)


@app.route('/project_details/<job_id>',methods=['POST','GET'])
def project_details(job_id):
    job = Job.query.filter(Job.mongo_id == job_id).first()
    about_company = Employer.query.filter(Employer.company_name == job.company_name).first().about_company
    session['job_id'] = job_id
    session['percentage_match'] = request.form['percentage_match']
    return render_template('pages/projectDetails.html',job = job,job_id=job_id,percentage_match = request.form['percentage_match'],about_company=about_company)

@app.route('/test_portal/<job_id>/<employee_id>',methods=['POST','GET'])
def test_portal(job_id,employee_id):
    session['job_id'] = job_id
    session['employee_id'] = employee_id
    portal_question = Job.query.filter(Job.mongo_id == session['job_id']).first().problem_statement
    return render_template('pages/test_screen.html',question = portal_question)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Error handlers.

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
