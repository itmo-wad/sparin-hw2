FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /app
COPY . . 

# install dependencies
RUN apt-get update
RUN apt-get install tk -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV FLASK_APP=src/app.py

ENTRYPOINT flask run -h 0.0.0.0