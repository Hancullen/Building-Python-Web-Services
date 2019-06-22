import os
import csv

from flask import Flask, render_template, request
from models import *
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

#app = Flask(__name__)

# Set up database (old version while using sql syntax)
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
#db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# link the Flask app with the database
db.init_app(app)

def main():
    f = open("flights_info.csv")
    reader = csv.reader(f)
    #old version using SQL syntax
    # for o, d, dur in reader:
    #     db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
    #     {"origin": o, "destination": d, "duration": dur}) #substitute values from CSV lines into SQL command
    #     print(f"Added flight from {o} to {d} lasting {dur} minutes.")
    # db.commit() # close the finished transaction
#Note: The colon notation used in db.execute() call is Postgres’ placeholder notation for values.
#This allows for the substitution of Python variables into SQL commands.
#Additionally, SQLAlchemy automatically takes care of sanitizing the values passed in.


    #new version using python classes and objects
    for o, dest, dur in reader:
    # NOTICE: "Flight" is the name of class, not table's name
        flights = Flight(origin=o, destination=dest, duration=dur)
        db.session.add(flights)
        print(f"Added flight from {o} to {dest} lasting {dur} minutes.")
    db.session.commit()



if __name__ == "__main__":
    #Allows command lines interact with Flask application
    with app.app_context():
        main()
