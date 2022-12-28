FROM python:3.10

RUN apt-get install -yqq --no-install-recommends \
    && pip install 'feedparser==6.0.10' \
    && pip install 'Telethon==1.25.0' \
    && pip install 'telethon-cryptg==0.0.4' \
    && pip install 'httpx==0.23.0' \
    && pip install 'rich' \
    && pip install 'mysql-connector-python'

WORKDIR /app

ADD main.py main.py
ADD config.py config.py
ADD tgParser.py tgParser.py
ADD rssParser.py rssParser.py
ADD session.session session.session
