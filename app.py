#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask,flash,Blueprint,render_template,request,redirect,session,url_for,abort,send_file,safe_join
from flask_bootstrap import Bootstrap
from flask_mongoalchemy import MongoAlchemy
from models import *
import bcrypt
import logging
from logging import Formatter, FileHandler
import os


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object('config')

@app.route('/')
def index():
    return render_template('forms/index.html')


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

                elif len(request.form['password'])<8: # password length check
                    flash('Please provide a password which is atleast 8 characters long')
                    return redirect(url_for('register',type='employer'))

                elif request.form['password'] != request.form['repeat_password']: # check passwords match
                    flash('Passwords mismatch. Please try again')
                    return redirect(url_for('register',type='employer'))

            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(10)) # hashing the password with a salt
            user_data = Employer(email = request.form['email'],password = hashed_password.decode('utf-8'),company_name = request.form['company_name'],first_name = request.form['first_name'],last_name = request.form['last_name'],jobs_posted = [])# storing the hashed password in the collection
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
                flash('No user registered with the specifed email')
                return redirect(url_for('index'))

            if bcrypt.hashpw(request.form['password'].encode('utf-8'),employee.password.encode('utf-8')) == employee.password.encode('utf-8'):
                session['email'] = request.form['email']
                session['user_type'] = type
                session['employee_id'] = str(employee.mongo_id)
                return redirect(url_for('employee_dashboard'))

        elif type == 'employer':# employer login
            employer = Employer.query.filter_by(email=request.form['email']).first()
            if employer is None:
                flash('No user registered with the specifed email')
                return redirect(url_for('index'))

            if bcrypt.hashpw(request.form['password'].encode('utf-8'),employer.password.encode('utf-8')) == employer.password.encode('utf-8'):
                session['email'] = request.form['email']
                session['user_type'] = type
                return 'logged in as %s' %session['email']

            else:
                flash('Incorrect Credentials Entered')
                return redirect(url_for('index'))

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

@app.route('/resume_builder')
def resume_builder():
    pass

@app.route('/employer_dashboard')
def employer_dashboard():
    pass

@app.route('/vacancies')
def vacancies():
        vacancies = Job.query.filter(Job.status == 'vacant').all()
        return render_template('pages/job_vacancies.html',vacancies = vacancies)

@app.route('/project_details/<int:job_id>',methods=['POST'])
def project_details(job_id):
    return render_template('pages/projectDetails.html',job_id=job_id)

@app.route('/test_portal/<int:job_id>/<int:employee_id>')
def test_portal(job_id,employee_id):
    session['job_id'] = job_id
    session['employee_id'] = employee_id

# upload to S3 using boto3
@app.route('/upload_files/<int:job_id>/<int:employee_id>')
def upload_files(job_id,employee_id):
    pass

@app.route('/photo_analysis/<int:job_id>/<int:employee_id>')
def photo_analysis(job_id,employee_id):
    pass

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
