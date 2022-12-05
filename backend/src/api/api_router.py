from fastapi import APIRouter
from . import project, dataset, experiment, fit_model, file_upload

api_router = APIRouter()
api_router.include_router(project.router, tags=["Project"])
api_router.include_router(dataset.router, tags=["Dataset"])
api_router.include_router(experiment.router, tags=["Experiment"])
api_router.include_router(file_upload.router, tags=["File"])
api_router.include_router(fit_model.router, tags=["AI-Model"])
