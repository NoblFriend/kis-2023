"""Provides data extractor from sqlite."""
from uuid import UUID
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime

from modules.models import Character, Geotag

class CharacterAppDatabase:
    def __init__(self, db_name="database/character_app.db"):
        self.conn = sqlite3.connect(db_name)
        sqlite3.register_adapter(UUID, lambda u: u.hex)
        self.create_tables()
        

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Characters (
                    id UUID PRIMARY KEY,
                    name TEXT NOT NULL
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Geotags (
                    id UUID PRIMARY KEY,
                    character_id UUID NOT NULL,
                    timestamp TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    FOREIGN KEY (character_id) REFERENCES Characters (id)
                );
            """)

    def add_character(self, character: Character):
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO Characters (id, name) VALUES (?, ?);",
                (character.id, character.name)
            )
            return cur.lastrowid 

    def get_characters(self) -> list[Character]:
        with self.conn:
            cur = self.conn.execute("SELECT id, name FROM Characters;")
            rows = cur.fetchall()
        return [Character(name=row[1], id=row[0]) for row in rows]

    def add_geotag(self, geotag: Geotag):
        with self.conn:
            self.conn.execute("INSERT INTO Geotags (id, character_id, timestamp, latitude, longitude) VALUES (?, ?, ?, ?, ?);",
                              (geotag.id, geotag.character_id, geotag.timestamp.isoformat(), geotag.latitude, geotag.longitude))

    def get_geotags(self, character_id: UUID) -> list[dict[str, datetime | float |  float]]:
        with self.conn:
            cur = self.conn.execute("SELECT timestamp, latitude, longitude FROM Geotags WHERE character_id = ?;", (character_id,))
            rows = cur.fetchall()
        return [{"timestamp": datetime.fromisoformat(row[0]), "latitude": row[1], "longitude": row[2]} for row in rows]


