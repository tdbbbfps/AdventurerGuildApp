from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models, schemas, database

router = APIRouter(
    prefix="/adventurers",
    tags=["adventurers"],
)

@router.post("/create", response_model=schemas.Adventurer)
async def create_adventurer(adventurer : schemas.AdventurerCreate, db : Session = Depends(database.get_database)):
    db_adventurer = models.Adventurer(
            name = adventurer.name,
            job_id = adventurer.job_id,
            level = adventurer.level,
            is_active = adventurer.is_active,
            gold = adventurer.gold
        )
    db.add(db_adventurer)
    db.commit()
    db.refresh(db_adventurer)
    return db_adventurer

@router.get("/read", response_model=list[schemas.Adventurer])
async def read_adventurers(db : Session = Depends(database.get_database)):
    adventurers = db.query(models.Adventurer).all()
    return adventurers