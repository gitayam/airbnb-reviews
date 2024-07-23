import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    HOST_NAME = os.getenv('HOST_NAME')
    HOME_DETAILS = os.getenv('HOME_DETAILS')
    MODEL = os.getenv('MODEL')
