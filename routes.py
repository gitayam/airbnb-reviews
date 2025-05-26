from flask import Blueprint, request, render_template, redirect, url_for, session, flash
import os
from review_generator import (
    generate_review as rg_generate_review,
    generate_private_note_to_guest as rg_generate_private_note_to_guest,
    generate_review_request as rg_generate_review_request,
    # We don't need convert_rating_to_description directly in routes.py
    # as the new rg_ functions will call it internally.
)

main = Blueprint('main', __name__)

def get_env_variable(var_name):
    return os.getenv(var_name) or session.get(var_name)

def load_configs_for_request():
    # Fetches configs from env/session.
    # Returns a dictionary of configs or None if essential ones are missing.
    api_key = get_env_variable("OPENAI_API_KEY")
    if not api_key:
        # Flash message will be handled by the route
        return None

    host_name = get_env_variable("HOST_NAME")
    home_details = get_env_variable("HOME_DETAILS")
    model_name = get_env_variable("MODEL") # Use model_name here

    if not all([host_name, home_details, model_name]):
        # Flash message will be handled by the route
        return None
        
    return {
        "api_key": api_key,
        "host_name": host_name,
        "home_details": home_details,
        "model_name": model_name # Changed from "model" to "model_name" for clarity
    }

@main.route('/')
def index():
    configs = load_configs_for_request()
    if configs is None:
        flash("Configuration is incomplete. Please set OpenAI API key, Host Name, Home Details, and Model on the setup page or in .env.")
        return redirect(url_for('main.setup'))
    return render_template('index.html')

@main.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        session['OPENAI_API_KEY'] = request.form['api_key']
        session['MODEL'] = request.form['model']
        session['HOST_NAME'] = request.form['host_name']
        session['HOME_DETAILS'] = request.form['home_details']
        return redirect(url_for('main.index'))
    api_key_set = 'OPENAI_API_KEY' in session
    return render_template('setup.html', api_key_set=api_key_set)

@main.route('/generate_review', methods=['POST'])
def generate_review_route():
    configs = load_configs_for_request()
    if configs is None:
        flash("Configuration is incomplete. Please set OpenAI API key, Host Name, Home Details, and Model on the setup page or in .env.")
        return redirect(url_for('main.setup'))

    name = request.form['name']
    rating = request.form['rating']
    communication = request.form['communication']
    cleanliness = request.form['cleanliness']
    house_rules = request.form['house_rules']
    comments = request.form['comments']
    private_note_input = request.form['private_note'] # Renamed to avoid conflict with generated note

    review = rg_generate_review(
        name, rating, communication, cleanliness, house_rules, comments,
        host_name=configs['host_name'], model=configs['model_name'], api_key=configs['api_key']
    )
    generated_note = rg_generate_private_note_to_guest(
        name, rating, communication, cleanliness, house_rules, private_note_input,
        host_name=configs['host_name'], home_details=configs['home_details'],
        model=configs['model_name'], api_key=configs['api_key']
    )
    review_request_message = rg_generate_review_request(
        name, review, generated_note, # Use the generated note for the request message
        host_name=configs['host_name'], model=configs['model_name'], api_key=configs['api_key']
    )
    return render_template('index.html', review=review, note=generated_note, review_request=review_request_message)

@main.route('/generate_review', methods=['GET'])
def generate_review_get():
    return redirect(url_for('main.index'))
