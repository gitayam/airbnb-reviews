import pyperclip
import os
from dotenv import load_dotenv
import argparse
from colorama import init
from review_generator import (
    convert_rating_to_description, # This is used directly in main()
    generate_review,
    generate_private_note_to_guest,
    generate_review_request
)

# Initialize colorama
init()

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
ITALIC = '\033[3m'

# Load environment variables from .env file
load_dotenv()

# Global variables like client, host_name, home_details, model
# are now initialized in review_generator.py and used by its functions.

def get_user_rating(prompt):
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
    comments = input(prompt)
    return comments

# Functions convert_rating_to_description, generate_review,
# generate_private_note_to_guest, and generate_review_request
# are now imported from review_generator.

def main():
    # Parse the command line arguments to get the name
    parser = argparse.ArgumentParser(description='Generate a guest review.')
    parser.add_argument('name', nargs='+', type=str, help='The name to be included in the review.')
    args = parser.parse_args()
    name = ' '.join(args.name)

    # Fetch configurations
    api_key = os.getenv("OPENAI_API_KEY")
    host_name = os.getenv("HOST_NAME")
    home_details = os.getenv("HOME_DETAILS")
    model_name = os.getenv("MODEL") # Use model_name

    if not api_key:
        print(f"{RED}{BOLD}Error: OPENAI_API_KEY not found in .env file.{ENDC}")
        return # Exit if API key is missing
    if not all([host_name, home_details, model_name]):
        print(f"{YELLOW}Warning: HOST_NAME, HOME_DETAILS, or MODEL might be missing from .env. Using default/empty values for missing ones.{ENDC}")
        # Allow to proceed but with a warning

    # Get the user's input for the ratings, comments, and private note.
    print('\n')
    rating = get_user_rating(f'Please provide an {BOLD}overall rating for {name}{ENDC}  (1 for bad, 2 for ok, 3 for good): ')
    print('\n' + '-' * 50 + '\n')
    communication = get_user_rating(f'{BOLD}Communication{ENDC} (1 for bad, 2 for ok, 3 for good): ')
    cleanliness = get_user_rating(f'{BOLD}Cleanliness{ENDC} (1 for bad, 2 for ok, 3 for good): ')
    house_rules = get_user_rating(f'Ability to Follow {BOLD}House Rules{ENDC} (1 for bad, 2 for ok, 3 for good): ')
    print('\n')
    comments = get_user_comment('Additional comments for Review (optional): ')
    private_note_comments = get_user_comment('Private Note Comments (optional): ')

    review = generate_review(
        name, rating, communication, cleanliness, house_rules, comments,
        host_name=host_name, model=model_name, api_key=api_key
    )
    print('\n' + '-' * 50 + '\n')
    print(review)
    pyperclip.copy(review)
    print('\n' + '-' * 50 + '\n')
    print(f'{BOLD}Generated Review Above{ENDC}')
    print(f'{ITALIC}The review has been copied to the clipboard.{ENDC}')
    print('Press enter to continue...')
    input()

    # 'private_note_comments' holds the user's input for the note.
    generated_private_note = generate_private_note_to_guest(
        name, rating, communication, cleanliness, house_rules, private_note_comments,
        host_name=host_name, home_details=home_details, model=model_name, api_key=api_key
    )
    print('\n' + '-' * 50 + '\n')
    print(generated_private_note)
    pyperclip.copy(generated_private_note)
    print(f'{ITALIC}The private note has been copied to the clipboard.{ENDC}')
    print('Generated Private Note Above')
    print('Press enter to continue...')
    input()
    
    review_request_message = generate_review_request(
        name, review, generated_private_note, # Use the generated note for the request
        host_name=host_name, model=model_name, api_key=api_key
    )
    print('\n' + '-' * 50 + '\n')
    print(review_request_message)
    pyperclip.copy(review_request_message)

if __name__ == "__main__":
    main()