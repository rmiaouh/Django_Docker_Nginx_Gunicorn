FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install python3-pip -y
ENV LC_ALL fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR.UTF-8
ENV LANG C.UTF-8
RUN apt-get install gunicorn3 -y
RUN \
  apt-get update && \
  apt-get install -y default-jre && \
  rm -rf /var/lib/apt/lists/*
COPY requirements.txt requirements.txt
COPY flaskapp /opt/
RUN pip3 install -r requirements.txt
WORKDIR /opt/
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
CMD ["gunicorn3", "-b", "0.0.0.0:8082", "app:app", "--workers=1", "--timeout=300"]
