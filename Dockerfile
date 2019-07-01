FROM python:3-alpine

COPY . /app 

WORKDIR /app
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev git
RUN python3 -m pip install -r requirements.txt --no-cache-dir && \
    python3 setup.py install && \
    apk --purge del .build-deps


WORKDIR /
RUN rm -fr /app

USER 10000
