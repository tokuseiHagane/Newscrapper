FROM python:3.10.5-slim-buster

RUN apt-get install -yqq --no-install-recommends 

WORKDIR /app

COPY ./ /app/

RUN pip install --no-cache-dir -r ./requirements.txt

ENV FLASK_APP=launch:app
