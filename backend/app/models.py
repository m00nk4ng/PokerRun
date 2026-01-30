from __future__ import annotations

from typing import Any, List, Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    first_name: Mapped[str] = mapped_column("firstName", String(100), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column("lastName", String(100), nullable=True)

    address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    town_or_city: Mapped[Optional[str]] = mapped_column("townOrCity", String(100), nullable=True)
    province_or_territory: Mapped[Optional[str]] = mapped_column("provinceOrTerritory", String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column("postalCode", String(20), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column("phoneNumber", String(30), nullable=True)

    created_at: Mapped[Any] = mapped_column(
        "createdAt", 
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[Any] = mapped_column(
        "updatedAt", 
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    hands: Mapped[List["Hand"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Hand(Base):
    __tablename__ = "hand"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    player_id: Mapped[int] = mapped_column(
        "playerId",
        ForeignKey("player.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Example value:
    # [{"suit": "S", "rank": "A"}, {"suit": "H", "rank": "10"}, ...]
    cards: Mapped[list] = mapped_column(JSONB, nullable=False)
    
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[Any] = mapped_column(
        "createdAt", 
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[Any] = mapped_column(
        "updatedAt", 
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    player: Mapped["Player"] = relationship(back_populates="hands")

