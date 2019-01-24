import os

PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DBNAME = os.getenv('PG_DBNAME')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_BATCH_SIZE = os.getenv('PG_BATCH_SIZE', 2000)
PG_AURANEST_TABLE = os.getenv('PG_AURANEST_TABLE', 'auranest')
PG_PLATSANNONS_TABLE = os.getenv('PG_PLATSANNONS_TABLE', 'platsannonser')
PG_SSLMODE = os.getenv('PG_SSLMODE', 'require')

AURANEST_FEED_URL = os.getenv('AURANEST_FEED_URL')
AURANEST_DETAILS_URL = os.getenv('AURANEST_DETAILS_URL')
AURANEST_USER = os.getenv('AURANEST_USER')
AURANEST_PASSWORD = os.getenv('AURANEST_PASSWORD')
LOADER_START_DATE = os.getenv('LOADER_START_DATE', '2018-01-01')

LA_FEED_URL = os.getenv('LA_FEED_URL')
LA_DETAILS_URL = os.getenv('LA_DETAILS_URL')

LA_EXPIRE_PATH = 'status.sista_publiceringsdatum'
AURANEST_EXPIRE_PATH = 'source.removedAt'
