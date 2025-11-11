from flask import Blueprint, redirect, render_template, request, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Creates a mapping for our authentication in urls
auth = Blueprint('auth', __name__)

# Returns login page 
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                # Display logged in successfully  
                flash('Logged in!', category='success')

                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                # Tell user wrong password, use right password
                flash('Wrong password, try again.', category='error')
        else:
            # Tell user password does not exist
            flash('Username does not exist.', category='error')

    return render_template('loginPage.html', user=current_user)

# Logs user out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Returns login page
@auth.route('/signUp', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            # Message saying user exists
            flash('Email already exists.', category='error')
        elif len(username) < 5:
            # Display error message
            flash('Error message: Username must be larger or equal to 4 characters', category='error') 
        elif len(password) < 9:
            # Display error message
            flash('Password must be larger or equal to 8 characters', category='error')
        else:
            # Add data to database
            new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))  
            
            db.session.add(new_user)  
            db.session.commit()
            login_user(new_user, remember=True)
            print("User logged in:", new_user.username)

            # Display success message
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))
        
    return render_template('signUpPage.html', user=current_user)