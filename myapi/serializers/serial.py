from dataclasses import dataclass
from datetime import datetime

@dataclass
class ID:
    id : int

@dataclass
class CreatedAt:
    created_at : datetime