FROM --platform=$BUILDPLATFORM python:3.10-alpine

RUN addgroup app && adduser -S -G app app

USER root
WORKDIR /app

COPY requirements.txt /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /app

RUN chown -R app:app .

USER app

EXPOSE 8000


CMD python3 manage.py makemigrations ; python3 manage.py migrate ; python3 -u manage.py runserver 0.0.0.0:8000





