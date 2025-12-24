from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models, schemas, database
from jobs_router import router as jobs_router
import uvicorn

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(
    title="冒險者公會後端API",
    description="這是一個用來管理冒險者資料的後端系統。",
    version="1.0.0",
)
app.include_router(jobs_router)
        
@app.get("/")
async def root():
    return {"message": "這裡是冒險者公會後端API的根目錄。"}

@app.post("/adventurers/create", response_model=schemas.Adventurer)
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

@app.put("/adventurers/update", response_model=schemas.Adventurer)
async update_adventurer(adventurer : AdventurerUpdate, db : Session = Depends(database.get_database)):
    db.execute(text("UPDATE adventurers set name = :name, job_id = :job_id, level = :level, is_active = :is_active where id = :id"), (
        adventurer.id,
        adventurer.name,
        adventurer.job_id,
        adventurer.level,
        adventurer.is_active
    ,))
    
    return
@app.get("/adventurers/read", response_model=list[schemas.Adventurer])
def read_adventurers(skip : int = 0, limit : int = 100, db : Session = Depends(database.get_database)):
    adventurers = db.query(models.Adventurer).offset(skip).limit(limit).all()
    return adventurers

@app.get('/adventurers/read_level', response_model=list[schemas.Adventurer])
async def read_adventurers_level_ge(ge : int = 0, db : Session = Depends(database.get_database)):
    adventurers = db.execute(text("""SELECT * FROM adventurers where level >= :ge"""), {"ge" : ge}).fetchall()
    return adventurers

@app.get('/adventurers/average_level')
async def get_adventurers_average_level(db : Session = Depends(database.get_database)):
    sql = text("""
                SELECT 
                    ROUND(AVG(a.level), 0) as Average Level
                FROM adventurers a
               """)
    result = db.execute(sql).fetchall()
    return result
    