from openai import OpenAI
import pyperclip
import os
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
host_name = os.getenv("HOST_NAME")
model = os.getenv("MODEL")

# Function to get user input
def get_user_input(prompt):
    return input(prompt)

# Function to generate review using OpenAI API
def generate_review(name, rating, comments):
    rating_description = {
        '1': 'bad',
        '2': 'ok',
        '3': 'good'
    }.get(rating, 'unknown')

    prompt = (
        f"Generate a brief, kind, polite, and professional guest review for Airbnb which I host based on the following details:\n"
        f"Name: {name}\n"
        f"Rating: {rating_description}\n"
        f"Comments: {comments}\n"
        "The review should be less than 4 sentences long."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
def generate_private_note_to_guest(name, rating, comments):
    rating_description = {
        '1': 'bad',
        '2': 'ok',
        '3': 'good'
    }.get(rating, 'unknown')

    prompt = (
        f"Generate a private note to the guest for Airbnb which I host based on the following details:\n"
        f"Name: {name}\n"
        f"Rating: {rating_description}\n"
        f"Comments: {comments}\n"
        f"My name is {host_name} and I am the host of this Airbnb listing.\n"
        "The note should be less than 3 sentences long, friendly, and should welcome the guest back anytime. the goal of the note should be influencing the guest to save our airbnb listing for next time."
    )

    response = client.chat.completions.create(
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

    rating = get_user_input('Please rate the service (1 for bad, 2 for ok, 3 for good): ')
    comments = get_user_input('Please provide any specific comments: ')

    review = generate_review(name, rating, comments)

    print('Generated Review:')
    print(review)

    pyperclip.copy(review)
    print('The review has been copied to the clipboard.')
    #prompt user to press any button to contiue before generating and printing and copying to clipboard the private  note
    print('Press enter to continue...')
    input()
    private_note = generate_private_note_to_guest(name, rating, comments)
    print('Generated Private Note:')
    print(private_note)
    pyperclip.copy(private_note)
    print('The private note has been copied to the clipboard.')

    

if __name__ == "__main__":
    main()
