import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# link the Flask app with the database
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route("/booking", methods=["POST"])
def booking():
    """Book a Flight"""
    # get form information
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid Flight Number")

    # Make sure the flight exists
    flight = Flight.query.get(flight_id)
    if not flight:
        return render_template("error.hmtl", message="There's no flight with that id")

    # Add passenger
    flight.add_passenger(name)
    return render_template("success.html")

@app.route("/flights_info")
def flights_info():
    fls = Flight.query.all()
    return render_template("flights_info.html", flights=fls )

@app.route("/flights_info/<int:flight_id>")
def flight_num(flight_id):
    """Details about a single flight"""
    # Make sure the flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.hmtl", message="There's no flight with that id")

    # Get all passengers
    #extract all passengers in this flight using relationship between table
    p = flight.passengers
    return render_template("flight_and_pax.html", flight=flight, passengers=p)


if __name__ == "__main__":
    app.run()
