from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.forms import LoginForm, RegistrationForm
from app.api import HydroHubsAPI

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        response = HydroHubsAPI.login_user(form.email.data, form.password.data)
        if response.status_code == 200:
            session['access_token'] = response.json()['access']
            session['user'] = response.json()['user']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.index'))
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords must match', 'danger')
        else:
            response = HydroHubsAPI.register_user(form.email.data, form.password.data)
            if response.status_code == 201:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('auth.login'))
            flash(response.json().get('detail', 'Registration failed'), 'danger')
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))