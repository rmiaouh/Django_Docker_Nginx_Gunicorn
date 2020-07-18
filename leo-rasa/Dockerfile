FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip
RUN apt-get install gunicorn3 -y

COPY requirements.txt requirements.txt
COPY flaskapp /opt/

RUN pip3 install -r requirements.txt
WORKDIR /opt/

CMD ["gunicorn3", "-b", "0.0.0.0:8087", "app:app", "--workers=1", "--timeout=300"]
