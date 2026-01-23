from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from .models import Person, Entry

from pokerkit import hands as pokerkit_hands

RANK_MAP = {
    "2": "2",
    "3": "3",
    "4": "4", 
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "T",
    "J": "J",
    "Q": "Q",
    "K": "K",
    "A": "A",
}

SUIT_MAP = {
    "S": "s",
    "H": "h",
    "D": "d",
    "C": "c",
}


def calculate_score(hands: list[dict]) -> int:
    """
    Convert API card payload into pokerkit PokerRunHand
    and return the numeric score.
    """
    if not hands:
        return 0

    try:
        hand_str = "".join(
            f"{RANK_MAP[card['rank']]}{SUIT_MAP[card['suit']]}"
            for card in hands
        )

        poker_hand = pokerkit_hands.PokerRunHand(hand_str)
        return poker_hand.entry.index

    except KeyError as e:
        raise ValueError(f"Invalid card value: {e}")

    except Exception as e:
        raise ValueError(f"Invalid poker hand: {e}")


async def create_person(db: AsyncSession, data: dict) -> Person:
    person = Person(**data)
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person


async def list_people(db: AsyncSession, limit: int = 100, offset: int = 0) -> list[Person]:
    stmt = select(Person).offset(offset).limit(limit).order_by(Person.id.desc())
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def create_entry(db: AsyncSession, person_id: int, hands: list[dict]) -> Entry:
    # Ensure person exists (simple guard)
    person = await db.get(Person, person_id)
    if not person:
        raise ValueError("Person not found")

    score = calculate_score(hands)

    entry = Entry(person_id=person_id, hands=hands, score=score)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


from sqlalchemy import select
from .models import Person, Entry

async def update_person(db: AsyncSession, person_id: int, data: dict):
    person = await db.get(Person, person_id)
    if not person:
        return None

    for key, value in data.items():
        setattr(person, key, value)

    await db.commit()
    await db.refresh(person)
    return person


async def delete_person(db: AsyncSession, person_id: int) -> bool:
    person = await db.get(Person, person_id)
    if not person:
        return False

    await db.delete(person)
    await db.commit()
    return True


async def update_entry(db: AsyncSession, entry_id: int, hands: list[dict] | None):
    entry = await db.get(Entry, entry_id)
    if not entry:
        return None

    if hands is not None:
        entry.hands = hands
        entry.score = calculate_score(hands)

    await db.commit()
    await db.refresh(entry)
    return entry


async def delete_entry(db: AsyncSession, entry_id: int) -> bool:
    entry = await db.get(Entry, entry_id)
    if not entry:
        return False

    await db.delete(entry)
    await db.commit()
    return True


async def list_entries(db: AsyncSession, limit: int = 100, offset: int = 0) -> list[Entry]:
    stmt = select(Entry).offset(offset).limit(limit).order_by(Entry.id.desc())
    res = await db.execute(stmt)
    return list(res.scalars().all())

async def list_ranked_entries(db: AsyncSession, limit: int = 100, offset: int = 0):
    stmt = (
        select(
            Entry.id.label("id"),
            Entry.person_id.label("person_id"),
            Entry.score.label("score"),
            Entry.hands.label("hands"),
            func.rank().over(order_by=Entry.score.desc()).label("rank"),
        )
        .order_by(Entry.score.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(stmt)
    rows = result.mappings().all()
    return [dict(r) for r in rows]


async def list_recent_entries_grouped(db: AsyncSession, limit: int = 20):
    stmt = (
        select(
            Entry.id.label("entry_id"),
            Person.id.label("person_id"),
            Person.first_name,
            Person.last_name,
            Person.address,
            Person.city,
            Person.province_or_territory,
            Person.postal_code,
            Person.phone_number,
            Person.created_at,
            Person.updated_at,
        )
        .join(Person, Person.id == Entry.person_id)
        .order_by(Entry.created_at.desc(), Entry.id.desc())
        .limit(limit)
    )

    rows = (await db.execute(stmt)).mappings().all()

    grouped: dict[int, dict] = {}

    for r in rows:
        pid = r["person_id"]
        if pid not in grouped:
            grouped[pid] = {
                "person": {
                    "id": pid,
                    "first_name": r["first_name"],
                    "last_name": r["last_name"],
                    "address": r["address"],
                    "city": r["city"],
                    "province_or_territory": r["province_or_territory"],
                    "postal_code": r["postal_code"],
                    "phone_number": r["phone_number"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                },
                "entryIds": [],
            }

        grouped[pid]["entryIds"].append(r["entry_id"])

    # Keeps "most recent people" ordering based on first appearance
    return list(grouped.values())