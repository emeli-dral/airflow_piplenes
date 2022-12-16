from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Optional

import os
import pickle

MODEL_FILE = os.getenv('MODEL_FILE', 'trees_regression.bin')

with open(MODEL_FILE, 'rb') as f_in:
    model = pickle.load(f_in)

app = FastAPI()

rides = {
	0 : {
	'PULocationID' : '43',
	'DOLocationID' : '151',
	'passenger_count' : '1.0',
	'trip_distance' : '1.01',
	'fare_forecast' : None
	}
}

class Ride(BaseModel):
	PULocationID: int
	DOLocationID: int
	passenger_count: int
	trip_distance: float
	fare_forecast: Optional[float] = None

@app.get("/get-ride/{ride_id}")
def get_ride(ride_id : int):
	return rides[ride_id]


@app.post("/add-ride/{ride_id}")
def add_ride(ride_id : int, ride : Ride):
	if ride_id in rides:
		return {"Error":"This ride already exists"}

	rides[ride_id] = ride
	return rides[ride_id]

@app.post("/predict-fare/{ride_id}")
def predict_fare(ride_id : int, ride : Ride):
	if ride_id in rides:
		return {"Error":"This ride already exists"}

	fare_forecast = model.predict([[ride.PULocationID, ride.DOLocationID, ride.passenger_count, ride.trip_distance]])

	rides[ride_id] = {
		"PULocationID": ride.PULocationID, 
		"DOLocationID": ride.DOLocationID, 
		"passenger_count": ride.passenger_count, 
		"trip_distance": ride.trip_distance,
		"fare_forecast": fare_forecast[0]
		}

	return rides[ride_id]
