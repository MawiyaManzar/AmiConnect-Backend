# Migration script to initialize AmiConnect schema
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DATABASE_URL')

with open('schema.sql', 'r') as f:
    schema_sql = f.read()

def run_migration():
    conn = psycopg2.connect(DB_URL)
    try:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
        print('Migration successful!')
    finally:
        conn.close()

if __name__ == '__main__':
    run_migration()
