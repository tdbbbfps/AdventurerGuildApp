from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(
    title="冒險者公會後端API",
    description="這是一個用來管理冒險者資料的後端系統。",
    version="1.0.0",
)
# Dependency: Get database connection.
def get_database():
    db = database.session()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
async def root():
    return {"message": "這裡是冒險者公會後端API的根目錄。"}

@app.post("/adventurers/create", response_model=schemas.Adventurer)
async def create_adventurer(adventurer : schemas.AdventurerCreate, database : Session = Depends(get_database)):
    database_adventurer = models.Adventurer(
        name = adventurer.name,
        class_id = adventurer.class_id,
        level = adventurer.level,
        is_active = adventurer.is_active,
        gold = adventurer.gold
    )
    database.add(database_adventurer)
    database.commit()
    database.refresh(database_adventurer)
    return database_adventurer

@app.get("/adventurers/read", response_model=list[schemas.Adventurer])
def read_adventurers(skip : int = 0, limit : int = 100, database : Session = Depends(get_database)):
    adventurers = database.query(models.Adventurer).offset(skip).limit(limit).all()
    return adventurers

@app.get('/adventurers/read_level', response_model=list[schemas.Adventurer])
async def read_adventurers_level_ge(ge : int = 0, database : Session = Depends(get_database)):
    adventurers = database.execute(text("""SELECT * FROM adventurers where level >= :ge"""), {"ge" : ge}).fetchall()
    return adventurers