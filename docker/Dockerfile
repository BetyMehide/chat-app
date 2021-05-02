# syntax=docker/dockerfile:1

FROM python:3.9
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /chat-app/src
COPY ./src/requirements.txt /chat-app/src
RUN pip install -r requirements.txt
COPY . /chat-app/
