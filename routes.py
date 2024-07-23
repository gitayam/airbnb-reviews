from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from openai import OpenAI
import os

main = Blueprint('main', __name__)

def get_env_variable(var_name):
    return os.getenv(var_name) or session.get(var_name)

client = None
host_name = None
home_details = None
model = None

def initialize_client():
    global client, host_name, home_details, model
    api_key = get_env_variable("OPENAI_API_KEY")
    if not api_key:
        return False
    client = OpenAI(api_key=api_key)
    host_name = get_env_variable("HOST_NAME")
    home_details = get_env_variable("HOME_DETAILS")
    model = get_env_variable("MODEL")
    return True

def convert_rating_to_description(rating):
    return {
        '1': 'Terrible',
        '2': 'Good',
        '3': 'Great'
    }.get(rating, 'unknown')

def generate_review(name, rating, communication, cleanliness, house_rules, comments):
    rating_description = convert_rating_to_description(rating)
    communication_description = convert_rating_to_description(communication)
    cleanliness_description = convert_rating_to_description(cleanliness)
    house_rules_description = convert_rating_to_description(house_rules)
    prompt = (
        f"Generate a brief, polite, and professional guest review for an Airbnb guest which I hosted based on the following details:\n"
        f"Name: {name}\n"
        f"Rating: {rating_description}\n"
        f"Communication: {communication_description}\n"
        f"Cleanliness: {cleanliness_description}\n"
        f"House Rules: {house_rules_description}\n"
        f"Comments: {comments}\n"
        "The review should be less than 4 sentences long. 1-3 emoji can be used. this review is written for other hosts to see."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_private_note_to_guest(name, rating, cleanliness, house_rules, private_note):
    rating_description = convert_rating_to_description(rating)
    cleanliness_description = convert_rating_to_description(cleanliness)
    house_rules_description = convert_rating_to_description(house_rules)
    
    # if private note is provide use the following prompt:
    if private_note:
        prompt = (
            f"Generate a private note (less than 4 sentences long, friendly) to the guest from Airbnb which I host based on the following details:\n"
            f"Guest Name: {name}\n"
            f"Guest Overall Rating: {rating_description}\n"
            f"Cleanliness: {cleanliness_description}\n"
            f"House Rules: {house_rules_description}\n"
            f"Include something about this in the output: {private_note} \n"
            f"Home Details: {home_details}\n"
            f"Our name is {host_name}, \n"
            "1-3 emoji can be used. The goal of the note should be influencing the guest to save our Airbnb listing for next time."
        )
    else:
        prompt = (
            f"Generate a private note (less than 4 sentences long, friendly where possible) to the guest from Airbnb which I host based on the following details:\n"
            f"Guest Name: {name}\n"
            f"Guest Overall Rating: {rating_description}\n"
            f"Cleanliness: {cleanliness_description}\n"
            f"House Rules: {house_rules_description}\n"
            f"Home Details: {home_details}\n"
            f"Our name to close out the message {host_name}, \n"
            "1-3 emoji can be used. The goal of the note should be influencing the guest to save our Airbnb listing for next time."
        )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@main.route('/')
def index():
    if not initialize_client():
        flash("Please set the OpenAI API key in the .env file or provide it on the setup page.")
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
    return render_template('setup.html')

@main.route('/generate_review', methods=['POST'])
def generate_review_route():
    if not initialize_client():
        flash("Please set the OpenAI API key in the .env file or provide it on the setup page.")
        return redirect(url_for('main.setup'))
    name = request.form['name']
    rating = request.form['rating']
    communication = request.form['communication']
    cleanliness = request.form['cleanliness']
    house_rules = request.form['house_rules']
    comments = request.form['comments']
    private_note = request.form['private_note']
    review = generate_review(name, rating, communication, cleanliness, house_rules, comments)
    note = generate_private_note_to_guest(name, rating, cleanliness, house_rules, private_note)
    return render_template('index.html', review=review, note=note)
