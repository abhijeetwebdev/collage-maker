import logging
from typing import List
from config import PATHS
from utils import helper
from fastapi import FastAPI, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import VersionedFastAPI, version

# init fast api server
app = FastAPI(debug=True)

# init api routes
@app.get('/')
@version(1)
def read_root():
    return 'API server is running here...'


# collage images accept and store
@app.post('/upload-images')
@version(1)
async def upload_images(target_image: UploadFile, source_images: List[UploadFile]):
    try:
        # fetch all images
        all_images = [target_image] + source_images
        
        # validate all image files
        helper.validate_image_files(all_images)
        
        # save files to the respective dir
        helper.save_files_to_dir(PATHS['UPLOADS'], all_images)
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({
                'status': 'success',
                'message': 'Images uploaded successfully.'
            })
        )
    except Exception as e:
        # handle error
        error = str(e)
        logging.error(f'Error: {error}')
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({
                'status': 'error',
                'message': error
            })
        )


# set versioning for the api
app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}'
)
