from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from joblib import load

import os.path
import pandas as pd
import pytz

''' API for a ML model to predict the fare of a NYC cab '''

# Instantiate app
app = FastAPI()

# allow all connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# root point
@app.get("/")
def index():
    return {"greeting": "Hello world"}

#predict method
@app.get("/predict")
def predict(request : Request):
    # Get request argument, put them in a dict
    request_args = dict(request.query_params)

    # Create dataframe from dict, add a random hardcoded key
    # Return a df with ordered columns
    df = pd.DataFrame(request_args, index=[0])
    df['key'] = '2013-07-06 17:18:00.000000119'
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]

    # create a datetime object from the user provided datetime
    df['pickup_datetime'] = df['pickup_datetime'].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    df['pickup_datetime'] = df['pickup_datetime'].apply(
        lambda x: eastern.localize(x, is_dst=None))

    df['pickup_datetime'] = df['pickup_datetime'].apply(
        lambda x: x.strftime("%Y-%m-%d %H:%M:%S UTC"))

    # load model, predict fare
    model = load(os.path.dirname(__file__) + '/../model.joblib')
    y_pred = model.predict(df)[0]

    return {'prediction' : y_pred}
