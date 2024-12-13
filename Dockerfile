FROM python:3.13-slim

RUN apt-get update && apt-get install -y supervisor procps gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

ARG SUPERVISORD_FILE
ENV SUPERVISORD_FILE=$SUPERVISORD_FILE
COPY $SUPERVISORD_FILE /etc/supervisor/conf.d/supervisord.conf

ARG ENTRYPOINT_FILE
COPY $ENTRYPOINT_FILE ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
EXPOSE 80

ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]