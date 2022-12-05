from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import database
from schema import schemas
from service import dataset_service as dataset_db
from service import project_service as proj_db

router = APIRouter()


@router.post("/datasets", response_model=schemas.Dataset)
def create_dataset(dataset: schemas.DatasetCreate, db: Session = Depends(database.get_db)):
    project = proj_db.get_single_project(db, dataset.project_id)
    if project is None:
        raise HTTPException(status_code=400, detail="Project not found")

    return dataset_db.create_dataset(db, dataset)


@router.get("/datasets", response_model=List[schemas.Dataset])
def get_datasets(project_id: Union[int, None] = None, db: Session = Depends(database.get_db)):
    return dataset_db.get_datasets(db=db, project_id=project_id)


@router.put("/datasets/{dataset_id}", response_model=schemas.Dataset)
def update_dataset(dataset_id: int, dataset: schemas.DatasetUpdate, db: Session = Depends(database.get_db)):
    project = proj_db.get_single_project(db, dataset.project_id)
    if project is None:
        raise HTTPException(status_code=400, detail="Project not found")
    dataset.id = dataset_id
    return dataset_db.update_dataset(db=db, dataset=dataset)


@router.get("/datasets/{dataset_id}", response_model=schemas.Dataset)
def get_dataset(dataset_id: int, db: Session = Depends(database.get_db)):
    return dataset_db.get_single_dataset(db=db, dataset_id=dataset_id)


@router.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(database.get_db)):
    dataset_db.delete_dataset(db=db, dataset_id=dataset_id)
    return
