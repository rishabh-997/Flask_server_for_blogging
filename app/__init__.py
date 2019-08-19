from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# The routes are the different URLs that the application implements

from app import routes
