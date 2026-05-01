import os
import psycopg2
from datetime import datetime
from app import config

def get_db_connection():
    """Returns a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS
        )
    except psycopg2.OperationalError as e:
        print(f"⚠️ [DB] Connection failed: {e}")
        return None

def init_db():
    """Initializes the analytics table as requested."""
    print("🐘 [DB] Initializing PostgreSQL Analytics table...")
    try:
        conn = get_db_connection()
        if not conn:
            print("⚠️ [DB] Skipping initialization - connection unavailable")
            return
        
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
        print("✅ [DB] Analytics table initialized")
    except Exception as e:
        print(f"⚠️ [DB] Initialization error: {e}")

def log_analytics(videos, errors, revenue):
    """Inserts a new analytics record."""
    try:
        conn = get_db_connection()
        if not conn:
            return
        
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
