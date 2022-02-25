# syntax=docker/dockerfile:1
FROM ubuntu:latest

#FROM python:3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# PIP
RUN apt-get update
RUN apt-get install -y python3.8 python3-pip --fix-missing

ENV DEBIAN_FRONTEND=noninteractive

# set work directory
WORKDIR /code

# wget
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

# Chrome
RUN apt-get update
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable

# Chrome webdriver
RUN apt-get install -yqq unzip
RUN apt-get install -y curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application", "--timeout", "600"]