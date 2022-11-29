from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import User, Collection
from app.auth import bp
from app.auth.validations import RegistrationValidation

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        # check authenticated user
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        else:
            return render_template('auth/register.html', title='Register Account')
    else:
        # get form data
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # check if passwords match
        if password != password_confirm: 
            # if passwords don't match, we want to redirect back to signup page so user can try again
            flash('There was an error. Passwords do not match')
            return redirect(url_for('auth.register'))

        # instantiate registration validation class
        validations = RegistrationValidation()

        # validate the username
        valid_username = validations.validate_username(username)
        if valid_username is not None:
            flash(valid_username)
            return redirect(url_for('auth.register'))

        # validate the email
        valid_email = validations.validate_email(email)
        if valid_email is not None:
            flash(valid_email)
            return redirect(url_for('auth.register'))
        
        # set default username
        if username:
            username = username
        else:
            username = email
        
        # create a user object, set password, set digest email for generating avatar, add user to the session and commit
        user = User(username=username, email=email)
        user.set_password(password)
        user.set_digest(email)
        db.session.add(user)
        db.session.commit()

        # create a default collection object, add collection to the session and commit
        collection = Collection(name='Default Collection', description='My default collection', visibility='Private', item_count=0, author=user)
        db.session.add(collection)
        db.session.commit()

        # redirect to login
        return redirect(url_for('auth.login'))
    
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        # check authenticated user
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        else:
            return render_template('auth/login.html', title='Login')
    else:
        # get input data
        username = request.form.get('username')
        password = request.form.get('password')

        # create a user object
        user = User.query.filter_by(username=username).first()

        # validate username/password
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
            
        # login and redirect to the dashboard
        login_user(user)
        return redirect(url_for('main.dashboard'))

# logout path
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))