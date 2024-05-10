import os
from flask import Flask, request, render_template, redirect, url_for, flash
from lib.database_connection import get_flask_database_connection
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from lib.space_repository import SpaceRepository
from lib.spaces import Space
from lib.user_repository import UserRepository
from lib.user import User
from lib.request_repository import RequestRepository
from lib.request import Request
import time


app = Flask(__name__)  # Create a Flask application instance
app.secret_key = 'team_mind'  # Set a secret key for the application 

login_manager = LoginManager()  # Create a LoginManager instance
login_manager.init_app(app)  # Initialize the LoginManager with the Flask application instance

@login_manager.user_loader  # Register a user loader function with the LoginManager
def load_user(user_id):  # Define a function to load a user given a user id
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    user_data = repo.find(user_id)
    if user_data:
        return User(user_data.id, user_data.name, user_data.email, user_data.password)
    return None

#LINK: http://127.0.0.1:5001/login


#-------------------------------------------------LOGIN page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']  # Retrieve the email from the form data
        password = request.form['password']  # Retrieve the password from the form data
        connection = get_flask_database_connection(app)
        users = UserRepository(connection)
        users2 = users.all()
        for user in users2:  # Iterate over the users dictionary
            if user.email == email and user.password == password:
                user = User(user.id, user.name ,email, password)
                login_user(user)
                return redirect("/spaces")
                # return render_template('dashboard.html', user=user)
        
        # If email or password is incorrect, show flash message
        flash('Invalid email or password. Please try again.', 'error')
        return redirect("/login")
    
    return render_template('login.html')

#-------------------------------------------------LOGIN page



#-------------------------------------------------SIGN UP page
@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        password_confirmation = request.form['password_conf']
        connection = get_flask_database_connection(app)
        users = UserRepository(connection)
        
        # Check if the email already exists
        if users.check_email_exists(email):
            flash('Email already exists. Please use a different email or sign in.', 'error')
            return redirect('/dashboard')  # Render the sign-up form with the flash message
        
        if password != password_confirmation:
            flash('Passwords are not the same')
            return redirect('/dashboard')

        # If the email doesn't exist, create the user
        users.create(User(None, name, email, password))
        flash('Account sign up successful!', 'success')  # Flash success message
        return redirect("/login")
        
    return redirect('/dashboard')

#-------------------------------------------------SIGN UP page

@app.route('/')
def goto_dashboard():  # Define a function to handle requests to the dashboard page
    return redirect("/dashboard")

#------------------------------------------------- DASHBOARD
@app.route('/dashboard')
def dashboard():  # Define a function to handle requests to the dashboard page
    return render_template("dashboard.html", errors = None)  # Return a greeting message with the current user's id and email
#------------------------------------------------- DASHBOARD


#-------------------------------------------------------------------- LOGOUT 
@app.route('/logout', methods=['GET'])  
def return_to_login():
    logout_user() 
    return redirect('/login') #Redirect back to login page
#-------------------------------------------------------------------- LOGOUT 


#-------------------------------------------------------------------- Incorrect password page
@app.route('/invalid_login', methods=['POST'])  
def return_to_login_after_incorrect_password():  # Define a function to handle requests to the login page after clicking return to login page
    return render_template("login.html") 
#-------------------------------------------------------------------- Incorrect password page


# Returns login page
@app.route('/sessions/new', methods=['GET'])
def get_login():
    return render_template('login.html')

# Returns page with list of all spaces
@app.route('/spaces', methods=['GET'])
@login_required
def get_spaces():
    connection = get_flask_database_connection(app)
    repo = SpaceRepository(connection)
    spaces = repo.all()
    # the following block is horrible. Works mostly. Oh well!
    if len(request.args) == 0 or request.args['start'] == "" or request.args['end'] == "":
        start = datetime.date(2000, 1, 1)
        end = datetime.date(3000, 1, 1)
    else:
        start_list = request.args['start'].split("-")
        start_list = [int(i) for i in start_list]
        end_list = request.args['end'].split("-")
        end_list = [int(i) for i in end_list]
        start = datetime.date(start_list[0], start_list[1], start_list[2])
        end = datetime.date(end_list[0], end_list[1], end_list[2])
    return render_template('spaces.html', spaces=spaces, start=start, end=end, username=current_user.name)

# Returns page to list a new space
@app.route('/spaces/new', methods=['GET'])
@login_required
def list_a_space():
    return render_template('space_form.html', username=current_user.name)

# Adds new space to webpage
@app.route('/spaces', methods=['POST'])
@login_required
def add_space():
    connection = get_flask_database_connection(app)
    repo = SpaceRepository(connection)
    space = Space(None, current_user.id, request.form['name'], request.form['description'], request.form['price_per_night'], request.form['start_date'], request.form['end_date']) # id, owner (current user id), name, desc., ppn, active (default: True)
    #if not space.is_valid():
     #   return render_template('space_form.html', space=space, errors=space.generate_errors()), 400
    
    repo.create(space)
    return redirect('/spaces')

# Returns page with space via id
@app.route('/spaces/<id>')
@login_required
def find_space(id):
    connection = get_flask_database_connection(app)
    repo = SpaceRepository(connection)
    space = repo.find(id)
    return render_template('spaces_id.html', space=space, username=current_user.name)

@app.route('/spaces/<id>', methods=['POST'])
@login_required
def create_request(id):
    connection = get_flask_database_connection(app)
    repo = RequestRepository(connection)
    repo.create(Request(current_user.id, id, request.form['start_date'], request.form['end_date'], "Pending"))
    return redirect('/spaces')

# Returns page with requests made AND requests recieved.
@app.route('/requests')
@login_required
def get_requests():
    connection = get_flask_database_connection(app)
    req_repo = RequestRepository(connection)
    reqs_from = req_repo.list_request_from_user(current_user.id)
    reqs_to = req_repo.list_request_to_user(current_user.id)
    return render_template('requests.html', reqs_from=reqs_from, reqs_to=reqs_to, username=current_user.name)

@app.route('/requests/<uid>-<sid>', methods=['POST'])
@login_required
def change_request_status(uid, sid):
    connection = get_flask_database_connection(app)
    req_repo = RequestRepository(connection)
    req_repo.update(request.form['response'], uid, sid)
    return redirect('/requests')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
