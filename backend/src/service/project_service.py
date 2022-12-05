from fastapi import HTTPException
from sqlalchemy.orm import Session

from model import models
from schema import schemas
from util import date_util, page_util


def get_projects(db: Session):
    return db.query(models.Project).all()


def create_project(db: Session, proj: schemas.ProjectCreate):
    created_date = date_util.get_current_date_str()
    db_project = models.Project(name=proj.name, description=proj.description, created_at=created_date,
                                updated_at=created_date)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, proj: schemas.ProjectUpdate):
    current_date = date_util.get_current_date_str()
    exist_project = db.query(models.Project).filter(models.Project.id == proj.id).first()
    if exist_project is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    exist_project.name = proj.name
    exist_project.description = proj.description
    exist_project.updated_at = current_date
    db.commit()
    return exist_project


def get_single_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def delete_project(db: Session, project_id: int):
    exist_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if exist_project is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(exist_project)
    db.commit()
