from typing import List
from dataclasses import dataclass


@dataclass
class CardDetails:
    card_id: str
    query: str
