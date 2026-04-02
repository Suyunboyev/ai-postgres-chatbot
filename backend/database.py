# database.py - Handles PostgreSQL connection and query execution
import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "chatbot"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "olim2004"),
        port=os.getenv("DB_PORT", "5432")
    )

def execute_query(sql: str):
    """Execute SELECT query safely and return list of dicts"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    try:
        cur.execute(sql)
        if cur.description:  # It's a SELECT query
            rows = cur.fetchall()
            return [dict(row) for row in rows]
        return None
    except Exception as e:
        return f"Database error: {str(e)}"
    finally:
        cur.close()
        conn.close()