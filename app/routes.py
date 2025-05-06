from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
import requests


customer_routes = Blueprint('customer', __name__, 
    template_folder='templates/customer')


# Dashboard sub-route (no separate Blueprint needed)
@customer_routes.route('/customer/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')  # Path matches file structure



@customer_routes.route('/customer/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Process form data
        form_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }
        
        # Validate passwords match
        if request.form.get('password') != request.form.get('confirm_password'):
            flash('Passwords do not match', 'error')
            return render_template('auth/signup.html', form_data=form_data)
        
        # Call your FastAPI backend
        try:
            response = requests.post(
                'https://wta-backend.onrender.com/api/customers/register/',
                json=form_data
            )
            
            if response.status_code == 201:
                # Return success flag instead of redirect
                return jsonify({
                    'status': 'success',
                    'message': 'Registration successful!',
                    'response': response.json(),
                })
            else:
                error = response.json().get('detail', 'Registration failed')
                return jsonify({
                    'status': 'error',
                    'message': error
                }), 400
        except requests.exceptions.RequestException as e:
            return jsonify({
                'status': 'error',
                'message': 'Connection error. Please try again.'
            }), 500
    
    # For GET requests
    return render_template('auth/signup.html')


@customer_routes.route('/customer/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # Prepare login data
        login_data = {
            'grant_type': 'password',
            'username': request.form['email'],  # email field maps to username
            'password': request.form['password'],
            'scope': '',
            'client_id': '',
            'client_secret': ''
        }

        try:

            # Call FastAPI login endpoint
            response = requests.post(
                'https://wta-backend.onrender.com/api/customers/login/',
                data=login_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            if response.status_code == 200:
                token_data = response.json()
                # Store token in session and return to client
                session['jwt_token'] = token_data['access_token']
                return jsonify({
                    'status': 'success',
                    'token': token_data['access_token'],
                    'redirect': url_for('customer.dashboard')
                })
            elif(response.status_code != 200):
                error = response.json().get('detail', 'Registration failed')
                return jsonify({
                    'status': 'error',
                    'message': error
                }), 400
            
            else:
            
                return jsonify(response.json()), response.status_code

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        
    # For GET requests
    return render_template('auth/login.html')