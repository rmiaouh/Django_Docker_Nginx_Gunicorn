FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

COPY requirements.txt requirements.txt
COPY flaskapp /opt/

RUN pip3 install -r requirements.txt
WORKDIR /opt/
RUN python3 -m spacy download en

CMD ["gunicorn3", "-b", "0.0.0.0:8081", "app:app", "--workers=3", "--timeout=300"]
