from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize app.
app = Flask(__name__)
# Allow Cross Orgin Requests for our app.
CORS(app)

# Database Setup.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create instance of the database.
db = SQLAlchemy(app)

