import os
import psycopg2
from datetime import datetime

# DB Config from environment
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "vartapravah")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    """Returns a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_db():
    """Initializes the analytics table as requested."""
    print("🐘 [DB] Initializing PostgreSQL Analytics table...")
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS analytics (
        id SERIAL PRIMARY KEY,
        videos_generated INT,
        errors INT,
        revenue FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def log_analytics(videos, errors, revenue):
    """Inserts a new analytics record."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO analytics (videos_generated, errors, revenue) VALUES (%s, %s, %s)",
            (videos, errors, revenue)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ [DB] Failed to log analytics: {e}")
