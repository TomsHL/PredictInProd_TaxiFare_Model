FROM python:3.8.12-buster

COPY api /api
COPY requirements.txt /requirements.txt
COPY model.joblib /model.joblib
COPY TaxiFareModel /TaxiFareModel
# COPY /home/tom/code/TomsHL/wagon-data-722-lardreau.json /wagon-data-722-lardreau.json

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --reload --host 0.0.0.0 --port $PORT
