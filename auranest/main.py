import logging
from auranest import loader
from auranest import postgresql

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def start():
    status = postgresql.system_status()
    next_ts = status['last_timestamp']
    next_id = None
    counter = 0
    while next_ts is not None:
        (next_ts, next_id, results) = loader.load(next_date=next_ts, next_id=next_id)
        counter += len(results)
        log.info("Downloaded %d documents. Total so far: %d" % (len(results), counter))
        if results:
            postgresql.bulk(results)


if __name__ == '__main__':
    start()
