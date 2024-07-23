[]: # Title: Airbnb Review Generator
[]: # Description: A script for generating polite and professional reviews for Airbnb guests using OpenAI's GPT.
# Airbnb Review Generator

This repository contains a script for generating polite and professional reviews for Airbnb guests using OpenAI's GPT. It supports both command-line and web-based interfaces, with the web interface designed to be hosted via Docker.

## Features

- **CLI Interface**: A simple script that prompts the user for details and generates a review.
- **Web Interface**: A user-friendly web application for generating reviews, which can be run locally or hosted using Docker.

## Setup

### Clone the Repository

```shell
git clone https://github.com/yourusername/airbnb-reviews.git
cd airbnb-reviews
```

### Create a Virtual Environment

1. **Create the virtual environment:**

    ```shell
    python3 -m venv venv
    ```

2. **Activate the virtual environment:**

    ```shell
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```shell
    pip3 install -r requirements.txt
    ```

### Set Your OpenAI API Key

Set your OpenAI API key in an environment variable `OPENAI_API_KEY`. You can create a `.env` file in the root directory of the project with the following content:

```env
OPENAI_API_KEY=your_openai_api_key
```

## Running the CLI Script

Run the script using Python:

```shell
python3 guest-reviews.py guest_name_here
```

## Running the Web Interface

### Using Docker

1. **Build the Docker image:**

    ```shell
    docker build -t airbnb-reviews-app .
    ```

2. **Run the Docker container:**

    ```shell
    docker-compose up -d --build --remove-orphans
    ```

3. **Access the Web Interface:**

    Open your browser and go to `http://localhost:5000`.

### Without Docker

1. **Ensure your virtual environment is activated.**

2. **Run the Flask application:**

    ```shell
    python3 app.py
    ```

3. **Access the Web Interface:**

    Open your browser and go to `http://localhost:5000`.
    
    This port might be different if set in the .env file

## Directory Structure

```plaintext
.
├── Dockerfile
├── README.md
├── .env-template
├── app.py
├── config.py
├── docker-compose.yml
├── guest-reviews.py
├── requirements.txt
├── routes.py
└── templates
    ├── index.html
    ├── note.html
    ├── review.html
    └── setup.html
```

## Example Usage (CLI)

1. When prompted, enter the name of the person/service.
2. Provide a rating (1 for bad, 2 for ok, 3 for good).
3. Add any specific comments you want to include in the review.
4. The generated review will be displayed and copied to the clipboard.

## Dependencies

The required dependencies are listed in the `requirements.txt` file:

```text
openai
pyperclip
python-dotenv
Flask
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

By following the steps outlined above, you can use the Airbnb Review Generator both from the command line and via a web interface. The Docker setup makes it easy to run the web application in any environment.
