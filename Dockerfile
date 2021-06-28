# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /dockersrc
COPY requirements.txt /dockersrc/
RUN pip install -r requirements.txt
COPY . /dockersrc/
