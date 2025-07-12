from flask import Blueprint, request, render_template, session, url_for, redirect, flash
from app.models import Register
from app import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # inputs from user:
        username = request.form.get('username')
        password = request.form.get('password')

        # exits user:
        user = Register.query.filter_by(username = username).first()

        if user:
            if password == user.password:
                session['user_id'] = user.id
                session['user'] = user.username
                flash('Login successful!', 'success')
                return redirect(url_for('task.view_task'))
            else:
                flash('Please enter correct username and password.', 'danger')
        else:
            flash('User not available, Please sign up.', 'danger')
            return redirect(url_for('auth.sign_up'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    flash('Logged out Successfully','info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/sign_up')
def sign_up():
    return render_template('register.html')

@auth_bp.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        con_password = request.form.get('confirm-password')

        if not(password == con_password):
            flash('Password mismatch. Try again!', 'danger')
            return redirect(url_for('auth.sign_up'))
        else:
            existing_user = Register.query.filter_by(username = username).first()  # For Unique username
            if existing_user:
                flash("Username not available!", 'danger')
                return redirect(url_for('auth.sign_up'))
            else:
                new_user = Register(username = username, password = password)
                db.session.add(new_user)
                db.session.commit()
                flash('Successfully signed in.', 'success')

    return redirect(url_for('auth.login'))


