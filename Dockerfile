FROM ubuntu:18.04

COPY . /app

RUN apt-get update -y \
  && apt-get install -y --fix-missing python3.7 python3-pip python3-setuptools postgresql-client


WORKDIR /app
RUN pip3 --trusted-host pypi.python.org install -r requirements.txt
RUN python3 setup.py install

WORKDIR /
RUN rm -fr /app
RUN apt-get clean

