from dataclasses import dataclass, field
import sqlite3
from typing import List, Optional


@dataclass
class Character:
    name: str
    id: Optional[int] = field(default=None)


class GandalfAppDatabase:
    def __init__(self, db_name="database/gandalf_app.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Geotags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    character_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    FOREIGN KEY (character_id) REFERENCES Characters (id)
                );
            """)

    def add_character(self, character: Character):
        with self.conn:
            cur = self.conn.execute("INSERT INTO Characters (name) VALUES (?);", (character.name,))
            return cur.lastrowid 

    def get_characters(self) -> List[Character]:
        with self.conn:
            cur = self.conn.execute("SELECT id, name FROM Characters;")
            rows = cur.fetchall()
        return [Character(name=row[1], id=row[0]) for row in rows]

    def add_geotag(self, character_id: int, timestamp: str, latitude: float, longitude: float):
        with self.conn:
            self.conn.execute("INSERT INTO Geotags (character_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?);",
                              (character_id, timestamp, latitude, longitude))

    def get_geotags(self, character_id: int) -> List[dict]:
        with self.conn:
            cur = self.conn.execute("SELECT timestamp, latitude, longitude FROM Geotags WHERE character_id = ?;", (character_id,))
            rows = cur.fetchall()
        return [{"timestamp": row[0], "latitude": row[1], "longitude": row[2]} for row in rows]

