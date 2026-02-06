from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


def to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

class HandCard(CamelModel):
    suit: str = Field(..., min_length=1, max_length=2)  # e.g. "S", "H", "D", "C"
    rank: str = Field(..., min_length=1, max_length=3)  # e.g. "A", "K", "10"


class PlayerCreate(CamelModel):
    first_name: str
    last_name: Optional[str] = None
    address: Optional[str] = None
    town_or_city: Optional[str] = None
    province_or_territory: Optional[str] = None
    postal_code: Optional[str] = None
    phone_number: Optional[str] = None


class PlayerOut(PlayerCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlayerCreateResponse(CamelModel):
    player: PlayerOut
    hand_id: int


# class PlayerWithHandIdsOut(BaseModel):
#     player: PlayerOut
#     handIds: list[int]


class HandCreate(CamelModel):
    player_id: int
    cards: List[HandCard]


class HandOut(CamelModel):
    id: int
    player_id: int
    cards: list
    score: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

        
class PlayerUpdate(CamelModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    town_or_city: str | None = None
    province_or_territory: str | None = None
    postal_code: str | None = None
    phone_number: str | None = None


class UpdatePlayerPayload(CamelModel):
    player: PlayerUpdate
    number_of_hands_to_add: int = 0
    hands_to_delete: List[int] = Field(default_factory=list)


class PlayerHandsResponse(CamelModel):
    player: PlayerOut
    hands: List[HandOut]


class HandUpdate(CamelModel):
    cards: list[HandCard] | None = None


class RankedHandOut(CamelModel):
    id: int
    player_id: int
    score: int
    rank: int
    cards: list

    class Config:
        from_attributes = True


class RecentPlayerOut(CamelModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    address: Optional[str] = None
    town_or_city: Optional[str] = None
    province_or_territory: Optional[str] = None
    postal_code: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class RecentEntrantOut(CamelModel):
    player: RecentPlayerOut
    hand_ids: List[int]

class LeaderboardHandOut(CamelModel):
    player: PlayerOut
    hand: HandOut
    leaderboardRank: int