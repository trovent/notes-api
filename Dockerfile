FROM python:3.13.3-slim

LABEL base.image="python:3.12-slim"
LABEL maintainer="t.nieberg@trovent.io"
LABEL version="1.0"
LABEL description="Docker image providing REST API for notebook web application"

COPY app/requirements.txt /app/

RUN pip install -r /app/requirements.txt

ADD app/*.py /app/

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0"]
