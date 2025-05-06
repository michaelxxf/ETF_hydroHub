import requests
from flask import current_app

class HydroHubsAPI:
    @staticmethod
    def register_user(email, password):
        url = f"{current_app.config['API_BASE_URL']}/customers/register/"
        response = requests.post(url, json={
            'email': email,
            'password': password
        })
        return response

    @staticmethod
    def login_user(email, password):
        url = f"{current_app.config['API_BASE_URL']}/customers/login/"
        response = requests.post(url, json={
            'email': email,
            'password': password
        })
        return response

    @staticmethod
    def get_user_profile(access_token):
        url = f"{current_app.config['API_BASE_URL']}/customers/me/"
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        return response