import logging
import threading
import requests
import sys

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_ad(ad_id, ts, results, index, url, user, pwd):
    fail_count = 0
    while True:
        try:
            r = requests.get(url, auth=(user, pwd),
                             params={'id': ad_id}, timeout=60)
            r.raise_for_status()
            ad = r.json()[0]
            if ad:
                ad['updatedAt'] = ts
                results[index] = ad
                break
        except requests.exceptions.RequestException as e:
            fail_count += 1
            log.warning('Failed to download ad "%s" %d times' % (ad_id, fail_count))
            if fail_count > 10:
                log.error("Unable to continue loading data from %s" % url, e)
                sys.exit(1)


def load(feed_url, details_url, next_date, next_id=None, username=None, password=None):
    payload = {'since': next_date}
    if next_id:
        payload['id'] = next_id

    log.info("Loading next batch starting at id: %s, date: %s" % (next_id, next_date))

    items = None
    try:
        if username and password:
            r = requests.get(feed_url,
                             auth=(username, password),
                             params=payload)
        else:
            r = requests.get(feed_url,
                             params=payload)
        r.raise_for_status()
        items = r.json()
    except requests.exceptions.RequestException as e:
        log.error("Failed to read from %s" % feed_url, e)
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
                                                                results, i,
                                                                details_url,
                                                                username,
                                                                password))
            threads[i].start()

        # Waiting for all threads to finish
        for thread in threads:
            thread.join()

    if not items:
        # Break the loop
        next_date = None

    return next_date, next_id, results
