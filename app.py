import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
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
		f"Welcome to the Hawai weather API<br/>"
		f"<br/>"
		f"Available Routes:<br/>"
		f"<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
#		f"/api/v1.0/startdate/2010-01-01"
	)

@app.route("/api/v1.0/precipitation")
def precipitation():
	
	results = session.query(Measurement.date, Measurement.prcp).all()
	
	session.close()
	
	return jsonify({date:prec for date,prec in results})


@app.route("/api/v1.0/stations")
def stations():
	#Query to get the station code and name
	total_rainfall= session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).distinct().all()
	session.close()
	return jsonify(total_rainfall)


@app.route("/api/v1.0/tobs")
def tobs():
	# Calculate the date 1 year ago from the last data point in the database
	last_data = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
	
	# Converting last date to date format
	last_data = dt.datetime.strptime(str(last_date[0]),'%Y-%m-%d')
	
	# get date one year before the last date
	one_year_data = last_date - dt.timedelta(days = 365)
	one_year_data
	
	results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_data).all()
	
	session.close()
	
	return jsonify({date:tobs for date,tobs in results})



if __name__ == '__main__':
	app.run(debug=True)
