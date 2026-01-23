from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from .db import get_db, quick_health_check
from . import crud, schemas
from .schemas import RankedEntryOut

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

# ---- People ----

@app.post("/people", response_model=schemas.PersonOut)
async def create_person(payload: schemas.PersonCreate, db: AsyncSession = Depends(get_db)):
    person = await crud.create_person(db, payload.model_dump())
    return person

@app.get("/people", response_model=list[schemas.PersonOut])
async def get_people(limit: int = 500, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await crud.list_people(db, limit=limit, offset=offset)

# ---- Entries ----

@app.post("/entries", response_model=schemas.EntryOut)
async def create_entry(payload: schemas.EntryCreate, db: AsyncSession = Depends(get_db)):
    try:
        hands_as_dicts = [h.model_dump() for h in payload.hands]
        entry = await crud.create_entry(db, payload.person_id, hands_as_dicts)
        return entry
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/entries", response_model=list[schemas.EntryOut])
async def get_entries(limit: int = 500, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await crud.list_entries(db, limit=limit, offset=offset)

# ---- Update Person ----
@app.put("/people/{person_id}", response_model=schemas.PersonOut)
async def update_person(
    person_id: int,
    payload: schemas.PersonUpdate,
    db: AsyncSession = Depends(get_db),
):
    person = await crud.update_person(
        db,
        person_id,
        payload.model_dump(exclude_unset=True),
    )
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


# ---- Delete Person ----
@app.delete("/people/{person_id}")
async def delete_person(person_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud.delete_person(db, person_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"status": "deleted"}


# ---- Update Entry ----
@app.put("/entries/{entry_id}", response_model=schemas.EntryOut)
async def update_entry(
    entry_id: int,
    payload: schemas.EntryUpdate,
    db: AsyncSession = Depends(get_db),
):
    hands = None
    if payload.hands is not None:
        hands = [h.model_dump() for h in payload.hands]

    entry = await crud.update_entry(db, entry_id, hands)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


# ---- Delete Entry ----
@app.delete("/entries/{entry_id}")
async def delete_entry(entry_id: int, db: AsyncSession = Depends(get_db)):
    ok = await crud.delete_entry(db, entry_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"status": "deleted"}


# ---- Ranked Entry ----
@app.get("/entries/ranked", response_model=list[RankedEntryOut])
async def get_ranked_entries(
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_ranked_entries(db, limit=limit, offset=offset)


# ---- Recent Entry ----
@app.get("/entries/recent", response_model=list[schemas.RecentEntrantOut])
async def get_recent_entries(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    limit = min(max(limit, 1), 500)
    return await crud.list_recent_entries_grouped(db, limit=limit)