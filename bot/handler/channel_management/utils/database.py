import sqlite3
from typing import Optional
from datetime import datetime

class ChannelDatabase:
    def __init__(self, db_path: str = "channels.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT UNIQUE,
                    username TEXT,
                    title TEXT,
                    added_date TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            conn.commit()

    def add_channel(self, channel_id: str, username: str, title: str) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO channels (channel_id, username, title, added_date) VALUES (?, ?, ?, ?)",
                    (channel_id, username, title, datetime.now())
                )
                return True
        except sqlite3.IntegrityError:
            return False

    def get_channel(self, channel_id: str) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM channels WHERE channel_id = ?", 
                (channel_id,)
            )
            result = cursor.fetchone()
            if result:
                return dict(zip([col[0] for col in cursor.description], result))
            return None
