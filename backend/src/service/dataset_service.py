from fastapi import HTTPException
from sqlalchemy.orm import Session

from model import models
from schema import schemas
from util import date_util, page_util


def get_datasets(db: Session, project_id: int):
    conditions = []
    if project_id is not None:
        conditions.append(models.Dataset.project_id == project_id)

    if len(conditions) > 0:
        return db.query(models.Dataset).filter(*conditions).all()

    return db.query(models.Dataset).all()


def create_dataset(db: Session, dataset: schemas.DatasetCreate):
    created_date = date_util.get_current_date_str()
    db_dataset = models.Dataset(name=dataset.name, description=dataset.description, project_id=dataset.project_id,
                                file_path=dataset.file_path, data=dataset.data,
                                version=0, created_at=created_date, updated_at=created_date)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def update_dataset(db: Session, dataset: schemas.DatasetUpdate):
    current_date = date_util.get_current_date_str()
    exist_dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset.id).first()
    if exist_dataset is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    exist_dataset.name = dataset.name
    exist_dataset.description = dataset.description
    exist_dataset.project_id = dataset.project_id
    exist_dataset.file_path = dataset.file_path
    exist_dataset.data = dataset.data
    exist_dataset.version = exist_dataset.version + 1
    exist_dataset.updated_at = current_date
    db.commit()
    return exist_dataset


def get_single_dataset(db: Session, dataset_id: int):
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()


def delete_dataset(db: Session, dataset_id: int):
    exist_dataset = db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()
    if exist_dataset is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(exist_dataset)
    db.commit()


def delete_datasets_by_project_id(db: Session, project_id: int):
    delete_num = db.query(models.Dataset).filter(models.Dataset.project_id == project_id).delete()
    if delete_num == 0:
        return
    db.commit()
