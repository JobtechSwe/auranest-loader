import logging
import threading
import requests
import sys
from auranest import settings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_ad(ad_id, ts, results, index):
    fail_count = 0
    while True:
        try:
            r = requests.get(settings.AURANEST_DETAILS_URL,
                             auth=(settings.AURANEST_USER, settings.AURANEST_PASSWORD),
                             params={'id': ad_id}, timeout=60)
            r.raise_for_status()
            auranest_ad = r.json()[0]
            if auranest_ad:
                auranest_ad['updatedAt'] = ts
                results[index] = auranest_ad
                break
        except requests.exceptions.RequestException as e:
            fail_count += 1
            log.warning('Failed to download ad "%s" %d times' % (ad_id, fail_count))
            if fail_count > 10:
                log.error("Unable to continue loading data from Auranest", e)
                sys.exit(1)


def load(next_date, next_id=None):
    payload = {'since': next_date}
    if next_id:
        payload['id'] = next_id

    log.info("Loading next batch starting at id: %s, date: %s" % (next_id, next_date))

    items = None
    try:
        r = requests.get(settings.AURANEST_FEED_URL,
                         auth=(settings.AURANEST_USER, settings.AURANEST_PASSWORD),
                         params=payload)
        r.raise_for_status()
        items = r.json()
    except requests.exceptions.RequestException as e:
        log.error("Failed to read from auranest", e)
    results = []

    if items:
        next_id = items[-1]['id']
        next_date = items[-1]['updatedAt']

        threads = [None] * len(items)
        results = [None] * len(items)

        for i in range(len(items)):
            item = items[i]
            threads[i] = threading.Thread(target=load_ad, args=(item['id'],
                                                                item['updatedAt'],
                                                                results, i,))
            threads[i].start()

        # Waiting for all threads to finish
        for thread in threads:
            thread.join()

    if not items:
        # Break the loop
        next_date = None

    return next_date, next_id, results
