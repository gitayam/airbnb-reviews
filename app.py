from flask import Flask
from routes import main as main_blueprint
from dotenv import load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# Load configuration from config.py
app.config.from_object('config.Config')

# Register blueprints
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT_NUMBER", 5000)))