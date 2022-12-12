FROM python:3.10.5-slim-buster

RUN apt-get install -yqq --no-install-recommends 

WORKDIR /service

COPY ./ /service/

RUN pip install --no-cache-dir -r ./requirements.txt

# ADD ./service/model model
# ADD ./service/controller controller
# ADD ./service/view view
# ADD ./service/__init__.py __init__.py
# ADD ./service/launch.py launch.py

# ADD bot.session bot.session
# ADD gazp.session gazp.session
