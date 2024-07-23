from openai import OpenAI
import pyperclip
import os
from dotenv import load_dotenv
import argparse
from colorama import init

# Define formatting
HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
host_name = os.getenv("HOST_NAME")
home_details = os.getenv("HOME_DETAILS")
model = os.getenv("MODEL")

# Function to get user input
def get_user_rating(prompt):
    # Get user input and validate that it is a valid rating
    # if no rating is provided, default to 2
    while True:
        try:
            rating = input(prompt)
            if rating == '':
                return '2'
            if rating not in ['1', '2', '3']:
                raise ValueError('Rating must be 1, 2, or 3.')
            return rating
        except ValueError as e:
            print(e)
def get_user_comment(prompt):
    # Get user input for comments
    # if no comments are provided, default to an empty string
    comments = input(prompt)
    return comments
    

def convert_rating_to_description(rating):
    # Convert rating to description based on the following scale:
    # change the rating to the corresponding description desired. This impacts the gpt prompt 
    return {
        '1': 'Terrible',
        '2': 'Good',
        '3': 'Great'
    }.get(rating, 'unknown')

def generate_review(name, rating, communication, cleanliness, houst_rules, comments):
    # this function generates a review for the guest based on the ratings and comments provided
    # Get rating description for rating, communication, cleanliness, and house rules
    rating_description = convert_rating_to_description(rating)
    communication_description = convert_rating_to_description(communication)
    cleanliness_description = convert_rating_to_description(cleanliness)
    houst_rules_description = convert_rating_to_description(houst_rules)

    prompt = (
        # this is the prompt that will be sent to the gpt model to generate the review
        f"Generate a brief, kind, polite, and professional guest review for Airbnb which I host based on the following details:\n"
        f"Name: {name}\n"
        f"Rating: {rating_description}\n"
        f"Communication: {communication_description}\n"
        f"Cleanliness: {cleanliness_description}\n"
        f"House Rules: {houst_rules_description}\n"
        f"Comments: {comments}\n"
        "The review should be less than 4 sentences long.One emoji can be used."
    )

    response = client.chat.completions.create(
        # this is the gpt model that will be used to generate the review and return the response
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def generate_private_note_to_guest(name, rating, communication, cleanliness, houst_rules, private_note):
    # Get rating description for rating, communication, cleanliness, and house rules
    rating_description = convert_rating_to_description(rating)
    communication_description = convert_rating_to_description(communication)
    cleanliness_description = convert_rating_to_description(cleanliness)
    houst_rules_description = convert_rating_to_description(houst_rules)

    prompt = (
        f"Generate a private note to the guest for Airbnb which I host based on the following details:\n"
        f"Guest Name: {name}\n"
        f"Guest Overall Rating: {rating_description}\n"
        f"Communication: {communication_description}\n"
        f"Cleanliness: {cleanliness_description}\n"
        f"House Rules: {houst_rules_description}\n"
        f"Priavte Note: {private_note}\n"
        f"Home Details: {home_details}\n"
        f"My name is {host_name} and I am the host of this Airbnb listing.\n"
        "The note should be less than 4 sentences long, friendly, and should welcome the guest back anytime. One emoji can be used. the goal of the note should be influencing the guest to save our airbnb listing for next time."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a guest review.')
    parser.add_argument('name', nargs='+', type=str, help='The name to be included in the review.')
    
    # Parse arguments
    args = parser.parse_args()
    name = ' '.join(args.name)
    # Get user input for ratings and comments
    rating = get_user_rating('Please rate the service (1 for bad, 2 for ok, 3 for good): ')
    print('\n' + '-' * 50 + '\n')
    # optional rating for communication, cleanliness, and house rules default to 2 if not provided
    communication = get_user_rating('{BOLD}Communication{ENDC} (1 for bad, 2 for ok, 3 for good): ')
    cleanliness = get_user_rating('{BOLD}Cleanliness{ENDC} (1 for bad, 2 for ok, 3 for good): ')
    houst_rules = get_user_rating('Ability to Follow {BOLD}House Rules{ENDC} (1 for bad, 2 for ok, 3 for good): ')
    comments = get_user_comment('Additional comments for Review (optional): ')
    private_note = get_user_comment('Private Note Comments (optional): ')
    # Print line breaks with seperators for formatting
    review = generate_review(name, rating, communication, cleanliness, houst_rules, comments)

    print('Generated Review:')
    print('\n' + '-' * 50 + '\n')
    print(review)
    pyperclip.copy(review)
    print('The review has been copied to the clipboard.')
    #prompt user to press any button to contiue before generating and printing and copying to clipboard the private  note
    
    print('\n' + '-' * 50 + '\n')
    print('\n' + '-' * 50 + '\n')
    print('Press enter to continue...')
    input()
    private_note = generate_private_note_to_guest(name, rating, communication, cleanliness, houst_rules, private_note)
    print('Generated Private Note:')
    print('\n' + '-' * 50 + '\n')
    print(private_note)
    pyperclip.copy(private_note)
    print('The private note has been copied to the clipboard.')

    

if __name__ == "__main__":
    main()
