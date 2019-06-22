import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# link the Flask app with the database
db.init_app(app)

def main():
    flights = Flight.query.all()
    for fl in flights:
        print(f"{fl.origin} to {fl.destination}, {fl.duration} minutes.")

if __name__ == "__main__":
    with app.app_context():
        main()
