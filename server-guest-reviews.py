from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, session, flash

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set secret key from .env file
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Replace 'default_secret_key' with a strong, random secret key

def get_env_variable(var_name):
    return os.getenv(var_name) or session.get(var_name)

# Initialize the OpenAI client with placeholders
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
        f"Generate a brief, kind, polite, and professional guest review for Airbnb which I host based on the following details:\n"
        f"Name: {name}\n"
        f"Rating: {rating_description}\n"
        f"Communication: {communication_description}\n"
        f"Cleanliness: {cleanliness_description}\n"
        f"House Rules: {house_rules_description}\n"
        f"Comments: {comments}\n"
        "The review should be less than 4 sentences long. One emoji can be used."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_private_note_to_guest(name, rating, communication, cleanliness, house_rules, private_note):
    rating_description = convert_rating_to_description(rating)
    communication_description = convert_rating_to_description(communication)
    cleanliness_description = convert_rating_to_description(cleanliness)
    house_rules_description = convert_rating_to_description(house_rules)
    prompt = (
        f"Generate a private note to the guest for Airbnb which I host based on the following details:\n"
        f"Guest Name: {name}\n"
        f"Guest Overall Rating: {rating_description}\n"
        f"Communication: {communication_description}\n"
        f"Cleanliness: {cleanliness_description}\n"
        f"House Rules: {house_rules_description}\n"
        f"Private Note: {private_note}\n"
        f"Home Details: {home_details}\n"
        f"My name is {host_name} and I am the host of this Airbnb listing.\n"
        "The note should be less than 4 sentences long, friendly, and should welcome the guest back anytime. One emoji can be used. The goal of the note should be influencing the guest to save our Airbnb listing for next time."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

@app.route('/')
def index():
    if not initialize_client():
        flash("Please set the OpenAI API key in the .env file or provide it on the setup page.")
        return redirect(url_for('setup'))
    return render_template('index.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        session['OPENAI_API_KEY'] = request.form['api_key']
        session['MODEL'] = request.form['model']
        session['HOST_NAME'] = request.form['host_name']
        session['HOME_DETAILS'] = request.form['home_details']
        return redirect(url_for('index'))
    return render_template('setup.html')

@app.route('/generate_review', methods=['POST'])
def generate_review_route():
    if not initialize_client():
        flash("Please set the OpenAI API key in the .env file or provide it on the setup page.")
        return redirect(url_for('setup'))
    name = request.form['name']
    rating = request.form['rating']
    communication = request.form['communication']
    cleanliness = request.form['cleanliness']
    house_rules = request.form['house_rules']
    comments = request.form['comments']
    private_note = request.form['private_note']
    review = generate_review(name, rating, communication, cleanliness, house_rules, comments)
    note = generate_private_note_to_guest(name, rating, communication, cleanliness, house_rules, private_note)
    return render_template('index.html', review=review, note=note)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT_NUMBER", 5000)))