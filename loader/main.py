import logging
import sys
from loader import loader, settings
from loader import postgresql

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def start_auranest():
    status = postgresql.system_status('auranest')
    next_ts = status['last_timestamp']
    next_id = None
    counter = 0
    while next_ts is not None:
        (next_ts,
         next_id,
         results) = loader.load(feed_url=settings.AURANEST_FEED_URL,
                                details_url=settings.AURANEST_DETAILS_URL,
                                next_date=next_ts, next_id=next_id,
                                username=settings.AURANEST_USER,
                                password=settings.AURANEST_PASSWORD)
        counter += len(results)
        log.info("Downloaded %d documents. Total so far: %d" % (len(results), counter))
        if results:
            postgresql.bulk(results, 'auranest')


def start_platsannonser():
    status = postgresql.system_status('platsannonser')
    next_ts = status['last_timestamp']
    next_id = None
    counter = 0
    while next_ts is not None:
        (next_ts,
         next_id,
         results) = loader.load(feed_url=settings.LA_FEED_URL,
                                details_url=settings.LA_DETAILS_URL,
                                next_date=next_ts, next_id=next_id)
        counter += len(results)
        log.info("Downloaded %d documents. Total so far: %d" % (len(results), counter))
        if results:
            postgresql.bulk(results, 'platsannonser')


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Usage: %s [platsannonser|auranest]" % sys.argv[0])
        sys.exit(0)
    if sys.args[1] == 'auranest':
        start_auranest()
    elif sys.argv[1] == 'platsannonser':
        start_platsannonser()
    else:
        print("Unknown dataset: %s" % sys.argv[1])
        sys.exit(1)
