from uuid import UUID
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from datetime import datetime

def _timestamp_validator(timestamp: datetime | str) -> datetime:
    if isinstance(timestamp, str):
        return datetime.fromisoformat(timestamp)
    if isinstance(timestamp, datetime):
        return timestamp


def none_to_default_str(field: str) -> str:
    return field or ''

@dataclass
class Character:
    name: str
    id: Optional[UUID] = field(default=None)
    
    def __post_init__(self):
        self.name = none_to_default_str(self.name)

@dataclass
class Geotag:
    character_id: UUID
    timestamp: datetime
    latitude: float
    longitude: float
    id: Optional[UUID] = field(default=None)
    
    def __post_init__(self):
        self.timestamp = _timestamp_validator(self.timestamp)