FROM python:3.8-slim as build_python

WORKDIR /data-science-onboard

COPY ./requirements.txt /data-science-onboard

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && \
    apt-get install -y python3-dev && \
    apt-get install -y build-essential && \
    apt-get install -y bash && \
    pip install pip --upgrade && \
    python -m venv /data-science-onboard/venv && \ 
    source /data-science-onboard/venv/bin/activate && pip install -r requirements.txt

COPY ./src /data-science-onboard/src
RUN cd /data-science-onboard/src && \
    pip install -r requirements.txt && \
    export FLASK_APP=services/api/controllers/movie_controller.py && \
    flask --app services/api/controllers/movie_controller.py run