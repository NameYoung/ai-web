from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import database
from schema import schemas
from service import dataset_service as dataset_db
from service import expriment_service as experiment_db
from service import project_service as proj_db

router = APIRouter()


@router.post("/experiments", response_model=schemas.Experiment)
def create_experiment(experiment: schemas.ExperimentCreate, db: Session = Depends(database.get_db)):
    project = proj_db.get_single_project(db, experiment.project_id)
    if project is None:
        raise HTTPException(status_code=400, detail="Project not found")

    dataset = dataset_db.get_single_dataset(db, experiment.dataset_id)
    if dataset is None:
        raise HTTPException(status_code=400, detail="Dataset not found")

    return experiment_db.create_experiment(db, experiment)


@router.get("/experiments", response_model=List[schemas.Experiment])
def get_experiments(project_id: Union[int, None] = None, dataset_id: Union[int, None] = None,
                    db: Session = Depends(database.get_db)):
    return experiment_db.get_experiments(db=db, project_id=project_id, dataset_id=dataset_id)


@router.put("/experiments/{experiment_id}", response_model=schemas.Experiment)
def update_experiment(experiment_id: int, experiment: schemas.ExperimentUpdate, db: Session = Depends(database.get_db)):
    project = proj_db.get_single_project(db, experiment.project_id)
    if project is None:
        raise HTTPException(status_code=400, detail="Project not found")

    dataset = dataset_db.get_single_dataset(db, experiment.dataset_id)
    if dataset is None:
        raise HTTPException(status_code=400, detail="Dataset not found")

    experiment.id = experiment_id
    return experiment_db.update_experiment(db=db, experiment=experiment)


@router.get("/experiments/{experiment_id}", response_model=schemas.Experiment)
def get_experiment(experiment_id: int, db: Session = Depends(database.get_db)):
    return experiment_db.get_single_experiment(db=db, experiment_id=experiment_id)


@router.delete("/experiments/{experiment_id}")
def delete_experiment(experiment_id: int, db: Session = Depends(database.get_db)):
    experiment_db.delete_experiment(db=db, experiment_id=experiment_id)
    return
