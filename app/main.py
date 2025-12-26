from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
import models, schemas, database
from jobs_router import router as jobs_router
from adventurers_router import router as adventurers_router
import uvicorn

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="冒險者公會後端API",
    description="這是一個用來管理冒險者資料的後端系統。",
    version="1.0.0",
)

app.include_router(adventurers_router)
app.include_router(jobs_router)
        
@app.get("/")
async def root():
    return {"message": "這裡是冒險者公會後端API的根目錄。"}