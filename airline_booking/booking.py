import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    #list all the flights
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight"""
    #get form information
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid Flight Number")

    # Make sure the flight exists
    if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="Incorrect Flight ID")

    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
    {"name": name, "flight_id": flight_id})
    db.commit()
    return render_template("success.html")

@app.route("/flights")
def flights():
    """Lists all the flights"""
    fls = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=fls)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """Lists dtails about a single flight"""

    #Make sure the flight exists
    flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("error.html")

    #Get all passengers
    p = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                    {"flight_id": flight_id}).fetchall()
    db.commit()
    return render_template("flight.html", flight=flight, passengers=p)

if __name__ == "__main__":
    app.run()
