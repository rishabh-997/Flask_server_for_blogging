from flask import Flask

app = Flask(__name__)

# The routes are the different URLs that the application implements

from app import routes
