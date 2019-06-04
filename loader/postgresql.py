import logging
from loader import settings
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
    log.info("PG_HOST not set, assuming local socket")
    pg_conn = psycopg2.connect(dbname=settings.PG_DBNAME,
                               user=settings.PG_USER)
else:
    pg_conn = psycopg2.connect(host=settings.PG_HOST,
                               port=settings.PG_PORT,
                               dbname=settings.PG_DBNAME,
                               user=settings.PG_USER,
                               password=settings.PG_PASSWORD,
                               sslmode=settings.PG_SSLMODE)


def get_new_pg_conn():
    if not settings.PG_HOST:
        log.info("PG_HOST not set, assuming local socket")
        new_conn = psycopg2.connect(dbname=settings.PG_DBNAME,
                                    user=settings.PG_USER)
    else:
        new_conn = psycopg2.connect(host=settings.PG_HOST,
                                    port=settings.PG_PORT,
                                    dbname=settings.PG_DBNAME,
                                    user=settings.PG_USER,
                                    password=settings.PG_PASSWORD,
                                    sslmode=settings.PG_SSLMODE)
    return new_conn


def query(sql, args):
    cur = pg_conn.cursor()
    cur.execute(sql, args)
    rows = cur.fetchall()
    cur.close()
    return rows


def table_exists(table):
    cur = pg_conn.cursor()
    cur.execute("select exists(select * from information_schema.tables "
                "where table_name=%s)", (table,))
    return cur.fetchone()[0]


def create_default_table(table):
    statements = (
        "CREATE TABLE {table} (id VARCHAR(64) PRIMARY KEY, doc JSONB, "
        "timestamp BIGINT, expires BIGINT)".format(table=table),
        "CREATE INDEX {table}_timestamp_idx ON {table} (timestamp)".format(table=table),
        "CREATE INDEX {table}_expires_idx ON {table} (expires)".format(table=table),
    )
    try:
        cur = pg_conn.cursor()
        for statement in statements:
            cur.execute(statement)
        cur.close()
        pg_conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        log.error("Failed to create database table: %s" % str(e))


def system_status(table):
    if not table_exists(table):
        create_default_table(table)
    cur = pg_conn.cursor()
    # Fetch last timestamp from table
    cur.execute("SELECT timestamp FROM " + table + " ORDER BY timestamp DESC LIMIT 1")
    ts_row = cur.fetchone()
    ts = _convert_to_timestring(ts_row[0]) \
        if ts_row else settings.LOADER_START_DATE
    cur.execute("SELECT id FROM " + table + " WHERE timestamp = %s",
                [convert_to_timestamp(ts)])
    id_rows = cur.fetchall()
    ids = [id_row[0] for id_row in id_rows]
    cur.close()
    return {'last_timestamp': ts, 'last_ids': ids}


def fetch_ad(ad_id, table):
    cur = pg_conn.cursor()
    cur.execute("SELECT * FROM " + table + " WHERE TRIM(id) = %s", [str(ad_id)])
    result = cur.fetchone()
    cur.close()
    return result


def update_ad(ad_id, doc, timestamp, table):
    cur = pg_conn.cursor()
    cur.execute("UPDATE " + table + " SET doc = %s, timestamp = %s WHERE TRIM(id) = %s", (json.dumps(doc),
                                                                                          convert_to_timestamp(
                                                                                              timestamp),
                                                                                          str(ad_id)))
    pg_conn.commit()
    cur.close()


def system_status_platsannonser(table):
    if not table_exists(table):
        create_default_table(table)
    cur = pg_conn.cursor()
    # Fetch last timestamp from table
    cur.execute("SELECT timestamp FROM " + table + " ORDER BY timestamp DESC LIMIT 1")
    ts_row = cur.fetchone()
    ts = ts_row[0] \
        if ts_row else convert_to_timestamp(settings.LOADER_START_DATE)
    cur.execute("SELECT TRIM(id) FROM " + table + " WHERE timestamp = %s",
                [ts])
    id_rows = cur.fetchall()
    ids = [id_row[0] for id_row in id_rows]
    cur.close()
    return {'last_timestamp': ts, 'last_ids': ids}


def bulk(items, table):
    start_time = time.time()
    adapted_items = [(item['id'].strip(),
                      convert_to_timestamp(item['updatedAt']),
                      convert_to_timestamp(item.get('expiresAt')),
                      json.dumps(item),
                      convert_to_timestamp(item['updatedAt']),
                      convert_to_timestamp(item.get('expiresAt')),
                      json.dumps(item)) for item in items if item]
    try:
        bulk_conn = get_new_pg_conn()
        cur = bulk_conn.cursor()
        cur.executemany("INSERT INTO " + table + " "
                                                 "(id, timestamp, expires, doc) VALUES (%s, %s, %s, %s) "
                                                 "ON CONFLICT (id) DO UPDATE "
                                                 "SET timestamp = %s, expires = %s, doc = %s", adapted_items)
        bulk_conn.commit()

    except psycopg2.DatabaseError as e:
        log.error('Could not bulk insert in database', e)
        sys.exit(1)
    finally:
        cur.close()
        bulk_conn.close()

    elapsed_time = time.time() - start_time

    log.info("Bulk inserted %d docs in: %s seconds." % (len(adapted_items), elapsed_time))


def convert_to_timestamp(date):
    if not date:
        return None
    if type(date) == int and date > 0:
        # Already a valid timestamp
        return date

    ts = 0
    for dateformat in [
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S%Z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d'
    ]:

        try:
            ts = time.mktime(time.strptime(date, dateformat)) * 1000
            log.debug("Converted date %s to %d" % (date, ts))
            break
        except ValueError as e:
            log.debug("Failed to convert date %s" % date, e)

    return int(ts)


def _convert_to_timestring(ts):
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')
