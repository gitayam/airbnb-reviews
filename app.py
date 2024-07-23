# app.py
from flask import Flask
from routes import main as main_blueprint
from dotenv import load_dotenv
import os

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Load configuration from config.py
app.config.from_object('config.Config')

# Enable debug mode for better error messages
app.debug = True

# Register blueprints
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT_NUMBER", 5000)))
