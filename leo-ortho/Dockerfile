FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y locales locales-all
ENV LC_ALL fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR.UTF-8

RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

COPY requirements.txt requirements.txt
COPY flaskapp /opt/

RUN pip3 install -r requirements.txt
WORKDIR /opt/

CMD ["gunicorn3", "-b", "0.0.0.0:8083", "app:app", "--workers=1", "--timeout=300"]




