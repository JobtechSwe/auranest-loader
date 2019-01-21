FROM python:3-alpine

COPY . /app 

WORKDIR /app
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev
RUN python3 -m pip install -r requirements.txt --no-cache-dir && \
    python3 setup.py install && \
    apk --purge del .build-deps

RUN apk add git
# show commit info
# RUN git log -1

WORKDIR /
RUN rm -fr /app

USER 10000
