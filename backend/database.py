import os
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv('DATABASE_URL')

def normalize(url):
    if not url:
        raise RuntimeError('DATABASE_URL não configurada.')
    return url.replace('postgres://','postgresql://',1) if url.startswith('postgres://') else url

@contextmanager
def get_connection():
    conn = psycopg2.connect(normalize(DATABASE_URL), cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(schema)
