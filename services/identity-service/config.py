import os
from dotenv import load_dotenv

load_dotenv() # This loads the variables from the .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # This is the connection string to our Docker database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')