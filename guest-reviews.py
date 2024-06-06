#guest-reviews.py
import openai
import pyperclip
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        f"Generate a brief, kind, polite, and professional guest review for airbnb based on the following details:\n"
        f"Name: {name}\n"
        f"Rating: {rating_description}\n"
        f"Comments: {comments}\n"
        "The review should be less than 4 sentences long."
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text.strip()

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
