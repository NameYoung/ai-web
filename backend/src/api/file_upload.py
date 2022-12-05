import pandas as pd
from fastapi import UploadFile, HTTPException, APIRouter
import numpy as np

from schema import schemas

router = APIRouter()


@router.post("/upload-file", response_model=schemas.FileUpload)
async def create_upload_file(file: UploadFile):
    try:
        contents = file.file.read()
        with open('./file/' + file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="File upload error")
    finally:
        file.file.close()

    source_data = pd.read_csv('./file/' + file.filename)

    return schemas.FileUpload(filename=file.filename, file_data=np.asarray(source_data[['x', 'y']]).tolist())
