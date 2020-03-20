FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV IN_YOYO_DOCKER 1

RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    sqlite3 \
    locales \
    cron \
    postgresql-client \
    gettext


RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile* /
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

WORKDIR /srv/yoyo

EXPOSE 8000
