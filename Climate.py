import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"       
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation by dates"""
    # Query
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>='2016-08-23').all()
     # Create a dictionary from the row data and append to a list of precipitation
    prcp_list = []
    for row in results:
        prcp_dict = {}
        prcp_dict["date"] = row.date
        prcp_dict["precipitation"] = row.prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def station():
    """Return a list of station"""
    # Query
    results = session.query(Station.station).all()
     # Create a dictionary from the row data and append to a list of stations
    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temp():
    """Return a list of temperature by dates"""
    # Query
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>='2016-08-23').all()
     # Create a dictionary from the row data and append to a list of temperature
    tobs = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["date"] = tob.date
        tobs_dict["temp"] = tob.tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    """Return list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
    # Query
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
     # Create a dictionary from the row data and append to a list of temperature
    tobs = []
    tobs_dict = {}
    tobs_dict["TMIN"] = results[0][0]
    tobs_dict["TAVG"] = results[0][1]
    tobs_dict["TMAX"] = results[0][2]
    tobs.append(tobs_dict)

    return jsonify(tobs)


@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    """Return list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
    # Query
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)) .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
     # Create a dictionary from the row data and append to a list of temperature
    tobs_1 = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["TMIN"] = tob[0]
        tobs_dict["TAVG"] = tob[1]
        tobs_dict["TMAX"] = tob[2]
        tobs_1.append(tobs_dict)

    return jsonify(tobs_1)


if __name__ == '__main__':
    app.run(debug=True)