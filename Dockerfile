FROM python:3.13.1-slim

RUN apt-get update && apt-get install -y supervisor procps gcc python3-dev default-libmysqlclient-dev build-essential pkg-config && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app

RUN chmod +x ./entrypoint.sh
EXPOSE 80

ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]