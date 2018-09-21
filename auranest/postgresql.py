import logging
from auranest import settings
from datetime import datetime
import psycopg2
import sys
import json
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

if not settings.PG_DBNAME or not settings.PG_USER:
    log.error("You must set environment variables for PostgresSQL (i.e. "
              "PG_HOST, PG_DBNAME, PG_USER and PG_PASSWORD.)")
    sys.exit(1)

if not settings.PG_HOST:
    log.info("Environment PG_HOST not set. Assuming local socket.")

pg_conn = psycopg2.connect(host=settings.PG_HOST,
                           port=settings.PG_PORT,
                           dbname=settings.PG_DBNAME,
                           user=settings.PG_USER,
                           password=settings.PG_PASSWORD)


def query(sql, args):
    cur = pg_conn.cursor()
    cur.execute(sql, args)
    rows = cur.fetchall()
    cur.close()
    return rows


def system_status():
    cur = pg_conn.cursor()
    # Fetch last timestamp from table
    cur.execute("SELECT timestamp FROM auranest ORDER BY timestamp DESC LIMIT 1")
    ts_row = cur.fetchone()
    ts = _convert_to_timestring(ts_row[0]) \
        if ts_row else '2018-01-01'  # Set a reasonable "epoch"
    cur.execute("SELECT id FROM auranest WHERE timestamp = %s",
                [_convert_to_timestamp(ts)])
    id_rows = cur.fetchall()
    ids = [id_row[0] for id_row in id_rows]
    cur.close()
    return {'last_timestamp': ts, 'last_ids': ids}


def bulk(items):
    start_time = time.time()
    adapted_items = [(item['id'],
                      _convert_to_timestamp(item['updatedAt']),
                      json.dumps(item),
                      _convert_to_timestamp(item['updatedAt']),
                      json.dumps(item)) for item in items if item]
    cur = pg_conn.cursor()
    cur.executemany("INSERT INTO auranest (id, timestamp, doc) VALUES (%s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE "
                    "SET timestamp = %s, doc = %s", adapted_items,)
    pg_conn.commit()
    elapsed_time = time.time() - start_time

    log.info("Bulk inserted %d docs in: %s seconds." % (len(adapted_items), elapsed_time))


def _convert_to_timestamp(date):
    ts = 0
    for dateformat in [
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S%Z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d']:
        try:
            ts = time.mktime(time.strptime(date, dateformat)) * 1000
            log.debug("Converted date %s to %d" % (date, ts))
            break
        except ValueError as e:
            log.debug("Failed to convert date %s" % date, e)

    return int(ts)


def _convert_to_timestring(ts):
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')
