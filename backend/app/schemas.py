from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class HandCard(BaseModel):
    suit: str = Field(..., min_length=1, max_length=2)  # e.g. "S", "H", "D", "C"
    rank: str = Field(..., min_length=1, max_length=3)  # e.g. "A", "K", "10"


class PersonCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_or_territory: Optional[str] = None
    postal_code: Optional[str] = None
    phone_number: Optional[str] = None


class PersonOut(PersonCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EntryCreate(BaseModel):
    person_id: int
    hands: List[HandCard]


class EntryOut(BaseModel):
    id: int
    person_id: int
    hands: list
    score: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

        
class PersonUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    city: str | None = None
    province_or_territory: str | None = None
    postal_code: str | None = None
    phone_number: str | None = None


class EntryUpdate(BaseModel):
    hands: list[HandCard] | None = None


class RankedEntryOut(BaseModel):
    id: int
    person_id: int
    score: int
    rank: int
    hands: list

    class Config:
        from_attributes = True


class RecentPersonOut(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_or_territory: Optional[str] = None
    postal_code: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class RecentEntrantOut(BaseModel):
    person: RecentPersonOut
    entryIds: List[int]