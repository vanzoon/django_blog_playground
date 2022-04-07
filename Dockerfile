FROM python:3.9-slim-buster
LABEL maintainer="vanzoon"

ENV PYTHONUNBUFFERED=1

ENV STATIC_ROOT /static

EXPOSE 8080

VOLUME /src
WORKDIR /src
COPY ./blogengine /src/ 
COPY requirements.txt /src/

RUN pip install --no-cache-dir -r ./requirements.txt

RUN ./manage.py collectstatic --noinput

