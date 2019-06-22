import os
import csv

#from flask import Flask, session
#from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#app = Flask(__name__)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("flights_info.csv")
    reader = csv.reader(f)
    for o, d, dur in reader:
        db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
        {"origin": o, "destination": d, "duration": dur}) #substitute values from CSV lines into SQL command
        print(f"Added flight from {o} to {d} lasting {dur} minutes.")
    db.commit() # close the finished transaction
#Note: The colon notation used in db.execute() call is Postgres’ placeholder notation for values.
#This allows for the substitution of Python variables into SQL commands.
#Additionally, SQLAlchemy automatically takes care of sanitizing the values passed in.


if __name__ == "__main__":
    main()
