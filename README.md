# airbnb-reviews
# Review Generator Script

This script prompts a user for a name, a rating (1, 2, 3 treated as bad, ok, good), and any specific comments. It then generates a brief, polite, and professional review using OpenAI's GPT and copies the review to the clipboard using `pyperclip`.

## Setup

1. Clone the repository or download the script files.
2. Create a virtual environment.
3. Activate the virtual environment.
4. Install the required dependencies.
5. Set your OpenAI API key in an environment variable `OPENAI_API_KEY`.

### Commands

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Running the Script

Run the script using Python:

```shell
python generate_review.py
```

## Requirements

- Python 3
- openai
- pyperclip

## Dependencies

The required dependencies are listed in the `requirements.txt` file:

```text
openai
pyperclip
```

## Example Usage

1. When prompted, enter the name of the person/service.
2. Provide a rating (1 for bad, 2 for ok, 3 for good).
3. Add any specific comments you want to include in the review.
4. The generated review will be displayed and copied to the clipboard.
