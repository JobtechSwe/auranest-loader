# job-ad-loaders

Loads ads from rest services into a database for later use by importers into Elasticsearch.

Local install
=================
    $ pip install -r requirements.txt

    $ python setup.py develop

Usage
=================
    load auranest ads to postgres:
    $ load-auranest

    load AF ads to postgres:
    $ load-platsannonser

Build docker
=================
sudo docker build -t jobadloaders:latest .


### Test

## Run unittests

    $ python3 -m pytest -svv -ra -m unit tests/
    
## Run integrationstests   
1. Create file /elastic-importers/tests/integration_tests/pytest_secrets.env

2. Add all needed environment variables in pytest_secrets.env, for example:
ES_USER=<elastic username>
ES_PWD=<elastic password>
ES_HOST=<elastic host, utan protokoll och port>
ES_PORT=9243

3. Run with command
    $ python3 -m pytest -svv -ra -m integration tests/