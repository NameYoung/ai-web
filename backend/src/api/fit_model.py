from math import sqrt

import numpy as np
import pandas as pd
from fastapi import APIRouter
from fastapi import HTTPException
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from schema import schemas

router = APIRouter()

# TODO 2022-12-02 make this as params
x_column_name = 'x'
y_column_name = 'y'
linear_type_str = 'LinearRegression'


@router.post("/fit-model", response_model=schemas.FitModelResult)
def fit_model(params: schemas.FitModelCreate):
    if params.model_type != 'LinearRegression':
        raise HTTPException(status_code=400, detail="Unsupported model type")

    source_data = pd.read_csv('./file/' + params.file_path)
    x_array = source_data[x_column_name]
    X = np.array(x_array).reshape(-1, 1)
    y = source_data[y_column_name]

    reg = LinearRegression()
    reg.fit(X, y)
    y_predict = reg.predict(X)

    # TODO data normalization

    model_index = schemas.ModelIndex(s2_score=r2_score(y, y_predict), mse=mean_squared_error(y, y_predict),
                                     mae=mean_absolute_error(y, y_predict),
                                     r_mse=sqrt(mean_squared_error(y, y_predict)))

    model_param = schemas.ModelParam(type=linear_type_str, copy_X=reg.copy_X, fit_intercept=reg.fit_intercept,
                                     n_jobs=reg.n_jobs, positive=reg.positive)

    predict_data = np.column_stack((x_array.tolist(), y_predict)).tolist()
    return schemas.FitModelResult(predict_data=predict_data, predict_index=model_index, model=model_param)
