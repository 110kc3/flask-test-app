FROM python:3.8-slim-buster

WORKDIR /app
COPY . /app

COPY requirements.txt requirements.txt 
# Install required library libmysqlclient (and build-essential for building mysqlclient python extension)
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

ENTRYPOINT  ["python"]

CMD ["main.py"]


