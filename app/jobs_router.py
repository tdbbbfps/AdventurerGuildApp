from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import models, schemas, database

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)

@router.get("/")
async def root():
    return {"message": "Here's jobs router's endpoint."}

@router.post("/create", response_model=schemas.Job)
async def create_job(job : schemas.JobCreate, db : Session = Depends(database.get_database)):
    db_job = models.Job(name=job.name)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/read", response_model=list[schemas.Job])
async def read_jobs(db : Session = Depends(database.get_database)):
    jobs = db.query(models.Job).all()
    return jobs
