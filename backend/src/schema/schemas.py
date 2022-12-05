from typing import List, Union

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: Union[str, None] = None


class ProjectFilter(BaseModel):
    page: int = 1
    size: int = 100


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    id: int


class Project(ProjectBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class SimpleDataset(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True


class DatasetBase(BaseModel):
    name: str
    project_id: int
    description: str
    file_path: str
    data: List[List[float]] = [[]]


class DatasetCreate(DatasetBase):
    pass


class DatasetUpdate(DatasetBase):
    id: int


class Dataset(DatasetBase):
    id: int
    version: int
    created_at: str
    updated_at: str
    project: Union[Project, None] = None

    class Config:
        orm_mode = True


class ModelIndex(BaseModel):
    s2_score: float
    mae: float
    mse: float
    r_mse: float


# model param abstract model
class ModelParamBase(BaseModel):
    type: str


class ModelParam(ModelParamBase):
    copy_X: bool
    fit_intercept: bool
    n_jobs: int = None
    normalize: bool = None
    positive: bool


class ExperimentBase(BaseModel):
    name: str
    project_id: int
    dataset_id: int
    source_data: List[List[float]] = [[]]
    predict_data: List[List[float]] = [[]]
    predict_index: ModelIndex
    model: ModelParam


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentUpdate(ExperimentBase):
    id: int


class Experiment(ExperimentBase):
    id: int
    created_at: str
    updated_at: str
    project: Union[Project, None] = None
    dataset: Union[SimpleDataset, None] = None

    class Config:
        orm_mode = True


class FitModelResult(BaseModel):
    predict_data: List[List[float]] = [[]]
    predict_index: ModelIndex
    model: ModelParam


class FitModelCreate(BaseModel):
    file_path: str
    model_type: str = 'LinearRegression'


class FileUpload(BaseModel):
    filename: str
    file_data: List[List[float]] = [[]]
