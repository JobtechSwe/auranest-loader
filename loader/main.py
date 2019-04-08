import logging
import sys
import itertools
import math
from loader import loader, loader_platsannonser, settings
from loader import postgresql

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def start_auranest():
    status = postgresql.system_status(settings.PG_AURANEST_TABLE)
    next_ts = status['last_timestamp']
    next_id = None
    counter = 0
    while next_ts is not None:
        (next_ts,
         next_id,
         results) = loader.load(feed_url=settings.AURANEST_FEED_URL,
                                details_url=settings.AURANEST_DETAILS_URL,
                                next_date=next_ts,
                                expires_path=settings.AURANEST_EXPIRE_PATH,
                                next_id=next_id,
                                username=settings.AURANEST_USER,
                                password=settings.AURANEST_PASSWORD)
        counter += len(results)
        log.info("Downloaded %d documents. Total so far: %d" % (len(results), counter))
        if results:
            postgresql.bulk(results, settings.PG_AURANEST_TABLE)


def start_platsannonser():
    last_ids, last_ts = get_system_status_platsannonser()

    bootstrap_needed = is_bootstrap_ads(last_ts)
    log.info('bootstrap_needed: %s' % bootstrap_needed)

    if bootstrap_needed:
        # Initial load from empty database
        load_and_save_bootstrap_ads()
        last_ids, last_ts = get_system_status_platsannonser()

    load_and_save_updated_ads(last_ts, last_ids)


def get_system_status_platsannonser():
    status = postgresql.system_status_platsannonser(settings.PG_PLATSANNONS_TABLE)
    last_ts = status['last_timestamp']
    last_ids = status['last_ids']
    log.info('last_ts: %s, last_ids: %s' % (last_ts, last_ids))
    return last_ids, last_ts


def load_and_save_updated_ads(last_ts, last_ids):
    updated_ad_ids = loader_platsannonser.fetch_updated_ads(last_ts, last_ids)
    log.info('Found %s ad ids to load...', len(updated_ad_ids))

    while len(updated_ad_ids) > 0:
        # Save found ads
        fetch_details_and_save(updated_ad_ids)

        # Check if there are more ads to fetch and save
        last_ids, last_ts = get_system_status_platsannonser()
        updated_ad_ids = loader_platsannonser.fetch_updated_ads(last_ts, last_ids)
        log.info('Found %s ad ids to load...', len(updated_ad_ids))


def load_and_save_bootstrap_ads():
    bootstrap_ad_ids = loader_platsannonser.fetch_bootstrap_ads()
    if bootstrap_ad_ids:
        fetch_details_and_save(bootstrap_ad_ids)


def grouper(n, iterable):
    iterable = iter(iterable)
    return iter(lambda: list(itertools.islice(iterable, n)), [])


def fetch_details_and_save(ad_ids):
    log.info('Fetching details for %s ads...' % len(ad_ids))
    nr_of_items_per_batch = int(settings.PG_BATCH_SIZE)
    nr_of_items_per_batch = min(nr_of_items_per_batch, len(ad_ids))
    nr_of_batches = math.ceil(len(ad_ids) / nr_of_items_per_batch)

    ad_batches = grouper(nr_of_items_per_batch, ad_ids)
    details_url = settings.LA_DETAILS_URL
    processed_ads_total = 0
    error_ids_total = []
    for i, ad_batch in enumerate(ad_batches):
        log.info('Processing batch %s/%s' % (i + 1, nr_of_batches))
        ad_batch_ids = [ad_data for ad_data in ad_batch]
        ad_details_data, error_ids = loader_platsannonser.execute_calls(ad_batch_ids, details_url,
                                                                        parallelism=settings.LA_DETAILS_PARALLELISM)
        results = list(ad_details_data.values())
        if results:
            log.info('Bulking %s ads to postgres' % len(results))
            postgresql.bulk(results, settings.PG_PLATSANNONS_TABLE)
        if len(error_ids) > 0:
            error_ids_total.extend(error_ids)
            log.error('Details batch. Could not load and save ad ids: %s' % error_ids)

        processed_ads_total = processed_ads_total + len(ad_batch)

        log.info('Processed %s/%s ads' % (processed_ads_total, len(ad_ids)))

    if len(error_ids_total) > 0:
        log.error('Total details batches. Could not load and save ad ids: %s' % error_ids_total)


def is_bootstrap_ads(last_ts):
    bootstrap_ads = False
    if last_ts == postgresql.convert_to_timestamp(settings.LOADER_START_DATE):
        bootstrap_ads = True
    return bootstrap_ads


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Usage: %s [platsannonser|auranest]" % sys.argv[0])
        sys.exit(0)
    if sys.argv[1] == 'auranest':
        start_auranest()
    elif sys.argv[1] == 'platsannonser':
        start_platsannonser()
    else:
        print("Unknown dataset: %s" % sys.argv[1])
        sys.exit(1)
