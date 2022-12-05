from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from model import models
from schema import schemas
from util import date_util, page_util


def get_experiments(db: Session, project_id: int, dataset_id: int):
    conditions = []
    if project_id is not None:
        conditions.append(models.Experiment.project_id == project_id)

    if dataset_id is not None:
        conditions.append(models.Experiment.dataset_id == dataset_id)

    if len(conditions) > 0:
        return db.query(models.Experiment).filter(*conditions).all()

    return db.query(models.Experiment).all()


def create_experiment(db: Session, experiment: schemas.ExperimentCreate):
    created_date = date_util.get_current_date_str()
    db_experiment = models.Experiment(name=experiment.name, project_id=experiment.project_id,
                                      dataset_id=experiment.dataset_id,
                                      source_data=jsonable_encoder(experiment.source_data),
                                      predict_data=jsonable_encoder(experiment.predict_data),
                                      predict_index=jsonable_encoder(experiment.predict_index),
                                      model=jsonable_encoder(experiment.model),
                                      created_at=created_date, updated_at=created_date)
    db.add(db_experiment)
    db.commit()
    db.refresh(db_experiment)
    return db_experiment


def update_experiment(db: Session, experiment: schemas.ExperimentUpdate):
    db_experiment = db.query(models.Experiment).filter(models.Experiment.id == experiment.id).first()
    if db_experiment is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    db_experiment.name = experiment.name
    db_experiment.project_id = experiment.project_id
    db_experiment.dataset_id = experiment.dataset_id
    db_experiment.source_data = jsonable_encoder(experiment.source_data)
    db_experiment.predict_data = jsonable_encoder(experiment.predict_data)
    db_experiment.predict_index = jsonable_encoder(experiment.predict_index)
    db_experiment.model = jsonable_encoder(experiment.model)
    db_experiment.updated_at = date_util.get_current_date_str()
    db.commit()
    return db_experiment


def get_single_experiment(db: Session, experiment_id: int):
    return db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()


def delete_experiment(db: Session, experiment_id: int):
    exist_experiment = db.query(models.Experiment).filter(models.Experiment.id == experiment_id).first()
    if exist_experiment is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(exist_experiment)
    db.commit()


def delete_experiments_by_project_id(db: Session, project_id: int):
    delete_num = db.query(models.Experiment).filter(models.Experiment.project_id == project_id).delete()
    if delete_num == 0:
        return
    db.commit()
