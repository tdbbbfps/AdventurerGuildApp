from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models, schemas, database
from jobs_router import jobs_router
import uvicorn

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(
    title="冒險者公會後端API",
    description="這是一個用來管理冒險者資料的後端系統。",
    version="1.0.0",
)
app.include_router(jobs_router)

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
async def create_adventurer(adventurer : schemas.AdventurerCreate, db : Session = Depends(get_database)):
    db_adventurer = models.Adventurer(
        name = adventurer.name,
        job_id = adventurer.job_id,
        level = adventurer.level,
        is_active = adventurer.is_active,
        gold = adventurer.gold
    )
    database.add(db_adventurer)
    database.commit()
    database.refresh(db_adventurer)
    return db_adventurer

@app.get("/adventurers/read", response_model=list[schemas.Adventurer])
def read_adventurers(skip : int = 0, limit : int = 100, db : Session = Depends(get_database)):
    adventurers = db.query(models.Adventurer).offset(skip).limit(limit).all()
    return adventurers

@app.get('/adventurers/read_level', response_model=list[schemas.Adventurer])
async def read_adventurers_level_ge(ge : int = 0, db : Session = Depends(get_database)):
    adventurers = db.execute(text("""SELECT * FROM adventurers where level >= :ge"""), {"ge" : ge}).fetchall()
    return adventurers

@app.get('/adventurers/average_level')
async def get_adventurers_average_level(db : Session = Depends(get_database)):
    sql = text("""
                SELECT 
                    ROUND(AVG(a.level), 0) as Average Level
                FROM adventurers a
               """)
    result = db.execute(sql).fetchall()
    return result
    