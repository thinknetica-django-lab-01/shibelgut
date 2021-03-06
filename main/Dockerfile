# pull official base image
FROM python:3.9-slim-buster

# set work directory
RUN mkdir /usr/src/main
WORKDIR /usr/src/main

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install postgresql-server-dev-all gcc python3-dev musl-dev netcat -y

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/main/requirements.txt
RUN pip install -r /usr/src/main/requirements.txt

# copy project
COPY . /usr/src/main

# copy entrypoint.sh
COPY entrypoint.sh /usr/src/main/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/main/entrypoint.sh"]
