from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from .db import get_db, quick_health_check
from . import crud, schemas
from .schemas import LeaderboardHandOut, PlayerWithHandIdsOut

app = FastAPI(title="poker_run_fastapi")

# DEV-friendly: allow localhost + common LAN IP ranges.
# If you want stricter production rules later, lock this down.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http:\/\/(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Hello World"}

@app.get("/ping")
async def ping():
    return {"status": "pong"}

@app.get("/health")
async def health():
    ok = await quick_health_check()
    return {"status": "ok" if ok else "db_down"}

@app.get("/db-time")
async def db_time(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT NOW()"))
    return {"db_time": str(result.scalar_one())}

# ---- Players ----

@app.post("/player", response_model=schemas.PlayerCreateResponse)
async def create_player(payload: schemas.PlayerCreate, db: AsyncSession = Depends(get_db)):
    player, hand_id = await crud.create_player_with_hand(db, payload.model_dump())
    return {"player": player, "handId": hand_id}

@app.get("/player", response_model=list[schemas.PlayerOut])
async def get_player(limit: int = 500, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await crud.list_players(db, limit=limit, offset=offset)

@app.get("/player/with-hands", response_model=list[PlayerWithHandIdsOut])
async def get_players_with_hands(
    limit: int = 500,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_players_with_hand_ids(db, limit=limit, offset=offset)

# ---- Hands ----

@app.post("/hand", response_model=schemas.HandOut)
async def create_hand(payload: schemas.HandCreate, db: AsyncSession = Depends(get_db)):
    try:
        cards_as_dicts = [h.model_dump() for h in payload.cards]
        hand = await crud.create_hand(db, payload.player_id, cards_as_dicts)
        return hand
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/hand", response_model=list[schemas.HandOut])
async def get_hands(limit: int = 500, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await crud.list_hands(db, limit=limit, offset=offset)

# ---- Update Player ----
@app.put("/player/{player_id}", response_model=schemas.PlayerOut)
async def update_player(
    player_id: int,
    payload: schemas.PlayerUpdate,
    db: AsyncSession = Depends(get_db),
):
    player = await crud.update_player(
        db,
        player_id,
        payload.model_dump(exclude_unset=True),
    )
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


# ---- Delete Player ----
@app.delete("/player/{player_id}")
async def delete_player(player_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud.delete_player(db, player_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"status": "deleted"}


# ---- Update Hand ----
@app.put("/hand/{hand_id}", response_model=schemas.HandOut)
async def update_hand(
    hand_id: int,
    payload: schemas.HandUpdate,
    db: AsyncSession = Depends(get_db),
):
    cards = None
    if payload.cards is not None:
        cards = [h.model_dump() for h in payload.cards]

    hand = await crud.update_hand(db, hand_id, cards)
    if not hand:
        raise HTTPException(status_code=404, detail="Hand not found")
    return hand


# ---- Delete Hand ----
@app.delete("/hand/{hand_id}")
async def delete_hand(hand_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud.delete_hand(db, hand_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Hand not found")
    return {"status": "deleted"}


# ---- Ranked Hand ----
@app.get("/hand/leaderboard", response_model=list[LeaderboardHandOut])
async def get_leaderboard_hands(
    limit: int = 600,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_leaderboard(db, limit=limit, offset=offset)


# ---- Recent Hand ----
@app.get("/hand/recent", response_model=list[schemas.RecentEntrantOut])
async def get_recent_hands(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    limit = min(max(limit, 1), 500)
    return await crud.list_recent_hands_grouped(db, limit=limit)