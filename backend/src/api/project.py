from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import database
from schema import schemas
from service import dataset_service as dataset_db
from service import expriment_service as experiment_db
from service import project_service as proj_db

router = APIRouter()


@router.post("/projects", response_model=schemas.Project)
def create_project(proj: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    return proj_db.create_project(db, proj)


@router.get("/projects", response_model=List[schemas.Project])
def get_projects(db: Session = Depends(database.get_db)):
    return proj_db.get_projects(db=db)


@router.put("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, proj: schemas.ProjectUpdate, db: Session = Depends(database.get_db)):
    proj.id = project_id
    return proj_db.update_project(db=db, proj=proj)


@router.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(database.get_db)):
    return proj_db.get_single_project(db=db, project_id=project_id)


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(database.get_db)):
    dataset_db.delete_datasets_by_project_id(db=db, project_id=project_id)
    experiment_db.delete_experiments_by_project_id(db=db, project_id=project_id)
    proj_db.delete_project(db=db, project_id=project_id)
    return
