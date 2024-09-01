import logging

import psycopg2

from app import create_app
from app.models import get_db_connection

user_table = """
            CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(32) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            date_created DATE DEFAULT CURRENT_TIMESTAMP
            );
            """

app = create_app()

with app.app_context():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(user_table)
    except psycopg2.DatabaseError as e:
        logging.error(e)
