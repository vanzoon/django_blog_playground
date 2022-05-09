FROM python:3.10-slim-buster
LABEL maintainer="vanzoon"

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

VOLUME /src
WORKDIR /src
COPY ./blogengine /src/ 
COPY requirements_prod.txt /src/
COPY README.md /src/

RUN pip install --no-cache-dir -r ./requirements_prod.txt

RUN ./manage.py collectstatic --noinput

