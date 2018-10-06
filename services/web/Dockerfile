# base image
FROM tiangolo/uwsgi-nginx-flask:python3.7

#https://github.com/tiangolo/uwsgi-nginx-flask-docker/blob/master/python3.7/Dockerfile

# install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# set working directory
WORKDIR /app

# add and install requirements
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /app
COPY ./services/web/prestart.sh /app/prestart.sh
COPY ./services/web/uwsgi.ini /app/uwsgi.ini
COPY ./services/web/main.py /app/main.py

ENV LISTEN_PORT 80