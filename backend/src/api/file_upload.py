import logging
import os

import numpy as np
import pandas as pd
from fastapi import UploadFile, HTTPException, APIRouter

from schema import schemas

router = APIRouter()
logging.basicConfig(level=logging.ERROR)


@router.post("/upload-file", response_model=schemas.FileUpload)
async def create_upload_file(file: UploadFile):
    base_path = os.path.abspath(".") + '/file/'

    is_exist = os.path.exists(base_path)
    if not is_exist:
        os.makedirs(base_path)

    try:

        contents = file.file.read()
        with open(base_path + file.filename, 'wb') as f:
            f.write(contents)

    except Exception as e:
        logging.error("Exception" + str(e))
        raise HTTPException(status_code=500, detail="File upload error")
    finally:
        file.file.close()

    source_data = pd.read_csv(base_path + file.filename)
    return schemas.FileUpload(filename=file.filename, file_data=np.asarray(source_data[['x', 'y']]).tolist())
