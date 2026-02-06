from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from .models import Player, Hand

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


def calculate_score(cards: list[dict]) -> int:
    """
    Convert API card payload into pokerkit PokerRunHand
    and return the numeric score.
    """
    if not cards:
        return 0

    try:
        hand_str = "".join(
            f"{RANK_MAP[card['rank']]}{SUIT_MAP[card['suit']]}"
            for card in cards
        )

        poker_hand = pokerkit_hands.PokerRunHand(hand_str)
        return poker_hand.entry.index

    except KeyError as e:
        raise ValueError(f"Invalid card value: {e}")

    except Exception as e:
        raise ValueError(f"Invalid poker hand: {e}")

# TODO: complete this next patch
def calculate_label(cards: list[dict]) -> str:
    """
    Convert API card payload into pokerkit PokerRunHand
    and return the numeric score.
    """
    if not cards:
        return ''

    try:
        hand_str = "".join(
            f"{RANK_MAP[card['rank']]}{SUIT_MAP[card['suit']]}"
            for card in cards
        )

        poker_hand = pokerkit_hands.PokerRunHand(hand_str)
        return poker_hand.entry.label.value

    except KeyError as e:
        raise ValueError(f"Invalid card value: {e}")

    except Exception as e:
        raise ValueError(f"Invalid poker hand: {e}")


async def create_player(db: AsyncSession, data: dict) -> Player:
    player = Player(**data)
    db.add(player)
    await db.commit()
    await db.refresh(player)
    return player


async def list_players(db: AsyncSession, limit: int = 100, offset: int = 0) -> list[Player]:
    stmt = select(Player).offset(offset).limit(limit).order_by(Player.id.desc())
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def create_hand(db: AsyncSession, player_id: int, cards: list[dict]) -> Hand:
    # Ensure player exists (simple guard)
    player = await db.get(Player, player_id)
    if not player:
        raise ValueError("Player not found")

    score = calculate_score(cards)

    hand = Hand(player_id=player_id, cards=cards, score=score)
    db.add(hand)
    await db.commit()
    await db.refresh(hand)
    return hand

async def create_player_no_commit(db: AsyncSession, data: dict) -> Player:
    player = Player(**data)
    db.add(player)
    await db.flush()
    await db.refresh(player)
    return player

async def create_hand_no_commit(db: AsyncSession, player_id: int, cards: list[dict]) -> Hand:
    player = await db.get(Player, player_id)
    if not player:
        raise ValueError("Player not found")

    score = calculate_score(cards)
    hand = Hand(player_id=player_id, cards=cards, score=score)
    db.add(hand)
    await db.flush()          # ensures hand.id is generated
    await db.refresh(hand)    # optional; flush usually enough for id
    return hand


async def create_player_with_hand(db: AsyncSession, player_data: dict):
    player = await create_player_no_commit(db, player_data)
    hand = await create_hand_no_commit(db, player.id, [])
    await db.commit()
    await db.refresh(player)
    await db.refresh(hand)
    return player, hand.id


async def list_players_with_hands(
    db: AsyncSession,
    limit: int = 500,
    offset: int = 0,
):
    # 1) get players
    players = (await db.execute(
        select(Player)
        .order_by(Player.id)
        .limit(limit)
        .offset(offset)
    )).scalars().all()

    if not players:
        return []

    player_ids = [p.id for p in players]

    # 2) get all hands for those players
    rows = (await db.execute(
        select(Hand)
        .where(Hand.player_id.in_(player_ids))
        .order_by(Hand.player_id, Hand.id)
    )).scalars().all()

    # group hands by player_id
    hands_by_player: dict[int, list[Hand]] = {pid: [] for pid in player_ids}
    for hand in rows:
        hands_by_player[hand.player_id].append(hand)

    # build response objects
    return [
        {
            "player": player,
            "hands": hands_by_player.get(player.id, []),
        }
        for player in players
    ]



async def update_player(db: AsyncSession, player_id: int, data: dict):
    player = await db.get(Player, player_id)
    if not player:
        return None

    for key, value in data.items():
        setattr(player, key, value)

    await db.commit()
    await db.refresh(player)
    return player


async def delete_player(db: AsyncSession, player_id: int) -> bool:
    player = await db.get(Player, player_id)
    if not player:
        return False

    await db.delete(player)
    await db.commit()
    return True


async def update_player_with_hands_ops(
    db: AsyncSession,
    player_id: int,
    player_update: dict,
    number_of_hands_to_add: int,
    hands_to_delete: list[int],
):
    # 1) Ensure player exists
    player = await db.get(Player, player_id)
    if not player:
        return None

    # 2) Update player fields (ignore id if present)
    player_update.pop("id", None)
    for key, value in player_update.items():
        setattr(player, key, value)

    # 3) Delete requested hands (only for this player)
    if hands_to_delete:
        await db.execute(
            delete(Hand).where(
                Hand.player_id == player_id,
                Hand.id.in_(hands_to_delete),
            )
        )

    # 4) Add N new hands (use existing no-commit helper style)
    if number_of_hands_to_add and number_of_hands_to_add > 0:
        for _ in range(number_of_hands_to_add):
            # New blank hand: cards=[], score computed as 0 by calculate_score([])
            await create_hand_no_commit(db, player_id, [])

    # 5) Commit once
    await db.commit()

    # 6) Refresh player
    await db.refresh(player)

    # 7) Fetch current hands list for this player (so response returns Hand rows)
    rows = (await db.execute(
        select(Hand).where(Hand.player_id == player_id).order_by(Hand.id)
    )).scalars().all()

    return {
        "player": player,
        "hands": list(rows),
    }


async def update_hand(db: AsyncSession, hand_id: int, cards: list[dict] | None):
    hand = await db.get(Hand, hand_id)
    if not hand:
        return None

    if cards is not None:
        hand.cards = cards
        hand.score = calculate_score(cards)

    await db.commit()
    await db.refresh(hand)
    return hand


async def delete_hand(db: AsyncSession, hand_id: int) -> bool:
    hand = await db.get(Hand, hand_id)
    if not hand:
        return False

    await db.delete(hand)
    await db.commit()
    return True


async def list_hands(db: AsyncSession, limit: int = 100, offset: int = 0) -> list[Hand]:
    stmt = select(Hand).offset(offset).limit(limit).order_by(Hand.id.desc())
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def list_recent_hands_grouped(db: AsyncSession, limit: int = 20):
    stmt = (
        select(
            Hand.id.label("hand_id"),
            Player.id.label("player_id"),
            Player.first_name,
            Player.last_name,
            Player.address,
            Player.town_or_city,
            Player.province_or_territory,
            Player.postal_code,
            Player.phone_number,
            Player.created_at,
            Player.updated_at,
        )
        .join(Player, Player.id == Hand.player_id)
        .order_by(Hand.created_at.desc(), Hand.id.desc())
        .limit(limit)
    )

    rows = (await db.execute(stmt)).mappings().all()

    grouped: dict[int, dict] = {}

    for r in rows:
        pid = r["player_id"]
        if pid not in grouped:
            grouped[pid] = {
                "player": {
                    "id": pid,
                    "first_name": r["first_name"],
                    "last_name": r["last_name"],
                    "address": r["address"],
                    "town_or_city": r["town_or_city"],
                    "province_or_territory": r["province_or_territory"],
                    "postal_code": r["postal_code"],
                    "phone_number": r["phone_number"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                },
                "hand_ids": [],
            }

        grouped[pid]["hand_ids"].append(r["hand_id"])

    return list(grouped.values())



async def list_leaderboard(db: AsyncSession, limit: int = 600, offset: int = 0):
    rank_col = func.rank().over(order_by=Hand.score.desc()).label("leaderboardRank")

    stmt = (
        select(Hand, Player, rank_col)
        .join(Player, Player.id == Hand.player_id)
        .order_by(Hand.score.desc(), Hand.created_at.desc(), Hand.id.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(stmt)
    rows = result.all()  # each row is (Hand, Player, rank)

    # Return plain dicts shaped exactly for Flutter
    return [
        {
            "player": player,
            "hand": hand,
            "leaderboardRank": rank_val,
        }
        for (hand, player, rank_val) in rows
    ]