FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV IN_YOYO_DOCKER 1

RUN apt-get update && apt-get install -y \
    libffi-dev \
    libgdal-dev \
    libssl-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    sqlite3 \
    locales \
    cron \
    postgresql-client \
    gettext

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /srv/yoyo

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile* /srv/yoyo/
RUN cd /srv/yoyo && pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000
