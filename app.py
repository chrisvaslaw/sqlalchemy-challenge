import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, select, join, text

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"-Return the JSON representation of your dictionary<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- Return a JSON list of stations from the dataset<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- Return a JSON list of temperature observations (TOBS) for the previous year<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive<br/>"
          )
#########################################################################################

# Build Routes-- Route 1
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of prior year rain totals from all stations"""

# Calculate the date one year from the last date in data set.
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                                   filter(Measurement.date > one_year).\
                                   order_by(Measurement.date).all()
    session.close()

# Create a dictionary from the row data and append to a list of precipitation data
    data = []
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict['Date'] = date[0]
        preciptiation_dict['Prcp'] = prcp[1]
        data.append(precipitation_dict)

# Return the JSON representation of your dictionary.
    return jsonify(data)

# Build Routes-- Route 2
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""

# Build a query to list all stations by name
all_stations = engine.execute('SELECT DISTINCT name FROM Station').fetchall()

# Convert list of tuples into normal list
all_station_list = list(np.ravel(all_stations))

# Return the JSON representation of your dictionary.
    return jsonify(all_station_list)

# Build Routes-- Route 3
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) for the previous year."""

# Calculate the date one year from the last date in data set.
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the temperature observations (TOBS) for the previous year
temp_obv = session.query(Measurement.date, Measurement.tobs).\
     filter(Measurement.date > one_year). \
            order_by(Measurements.date).all()
            session.close()

# Return the JSON representation of your list
    return jsonify(temp_obv)

# Build Routes-- Route 4
@app.route("/api/v1.0/start")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""

# Calculate the date one year from the last date in data set.
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Calculate the minimum temperature, the average temperature, and the max temperature for the start date
temp_max_start = session.query(func.max(Measurement.tobs)).filter((Measurement.date > one_year))
temp_min_start = session.query(func.min(Measurement.tobs)).filter((Measurement.date > one_year))
temp_avg_start = session.query(func.avg(Measurement.tobs)).filter((Measurement.date > one_year))

stats_data_start = [temp_max_start.all(), temp_min_start.all(), temp_avg_start.all()]
session.close()

stats_list_start = list(np.ravel(stats_data_start))

# Return the JSON representation of your list
    return jsonify(stats_list)

# Build Routes-- Route 5
@app.route("/api/v1.0/start/end")
def end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""

# Calculate the date one year from the last date in data set.
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Calculate the minimum temperature, the average temperature, and the max temperature for the start date
temp_max_end = session.query(func.max(Measurement.tobs)).filter((Measurement.date <= one_year))
temp_min_end = session.query(func.min(Measurement.tobs)).filter((Measurement.date <= one_year))
temp_avg_end = session.query(func.avg(Measurement.tobs)).filter((Measurement.date <= one_year))

stats_data_end = [temp_max_end.all(), temp_min_end.all(), temp_avg_end.all()]
session.close()

stats_list_end = list(np.ravel(stats_data_end))

# Return the JSON representation of your list
    return jsonify(stats_list_end)

# End Flask
if __name__ == '__main__':
    app.run(debug=True)
