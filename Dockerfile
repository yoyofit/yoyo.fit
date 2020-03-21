FROM python:3.7
MAINTAINER Arseny Sokolov <me@arsen.pw>

ENV PYTHONUNBUFFERED 1
ENV IN_YOYO_DOCKER 1
ENV DOCKERIZE_VERSION v0.6.1
ENV DJANGO_SUPERUSER_NAME Admin
ENV DJANGO_SUPERUSER_EMAIL admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD password
ENV DJANGO_SETTINGS_MODULE yoyoproject.settings

RUN apt-get update && apt-get install -y \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    sqlite3 \
    locales \
    cron \
    postgresql-client \
    gettext \
    wget

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz


RUN pip install --upgrade pip && pip install pipenv gunicorn

COPY Pipfile* /
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY entrypoint.sh /

COPY . /srv/yoyo
WORKDIR /srv/yoyo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["runserver", "0.0.0.0:8000"]
