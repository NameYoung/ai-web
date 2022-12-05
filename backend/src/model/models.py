from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from database import Base
from util import date_util


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(String, default=date_util.get_current_date_str())
    updated_at = Column(String, default=date_util.get_current_date_str())


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey("project.id"))
    description = Column(String)
    file_path = Column(String)
    data = Column(JSON)
    created_at = Column(String, default=date_util.get_current_date_str())
    updated_at = Column(String, default=date_util.get_current_date_str())
    version = Column(Integer, default=0)
    project = relationship("Project")


class Experiment(Base):
    __tablename__ = "experiment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    project_id = Column(Integer, ForeignKey("project.id"))
    dataset_id = Column(Integer, ForeignKey("dataset.id"))
    source_data = Column(JSON)
    predict_data = Column(JSON)
    predict_index = Column(JSON)
    model = Column(JSON)
    created_at = Column(String, default=date_util.get_current_date_str())
    updated_at = Column(String, default=date_util.get_current_date_str())
    project = relationship("Project")
    dataset = relationship("Dataset")
