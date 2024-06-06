from openai import OpenAI
import pyperclip
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        f"Generate a brief, kind, polite, and professional guest review for Airbnb based on the following details:\n"
        f"Name: {name}\n"
        f"Rating: {rating_description}\n"
        f"Comments: {comments}\n"
        "The review should be less than 4 sentences long."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def main():
    name = get_user_input('Please enter the name: ')
    rating = get_user_input('Please rate the service (1 for bad, 2 for ok, 3 for good): ')
    comments = get_user_input('Please provide any specific comments: ')

    review = generate_review(name, rating, comments)

    print('Generated Review:')
    print(review)

    pyperclip.copy(review)
    print('The review has been copied to the clipboard.')

if __name__ == "__main__":
    main()
