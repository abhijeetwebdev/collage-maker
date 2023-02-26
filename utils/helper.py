import os
import cv2
import shutil
import logging
from config import PATHS, ALLOWED_IMAGE_TYPES

# setup logging
def setup_logging():
    logging.basicConfig(
        filename = './storage/collage-maker.log',
        format = '%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s',
        level = logging.INFO
    )


# get the list of source images from uploads dir
def get_files_from_dir(dir=None):
    if dir is None:
        dir = PATHS['UPLOADS']
    
    try:
        file_names = []
        for filename in os.listdir(dir):
            file = cv2.imread(os.path.join(dir, filename))
            if file is not None:
                file_names.append(filename)
        
        return file_names
    except Exception as e:
        raise Exception(f'Failed to load files from {dir}, Error: {str(e)}')


# save image files to the directory
def save_files_to_dir(dir=None, files=[]):
    if dir is None:
        dir = PATHS['UPLOADS']
    
    for file in files:
        try:
            destination = f'{dir}/{file.filename}'
            logging.info(f'Saving file to "{destination}"')
            with open(destination, 'wb+') as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            logging.error(f'Failed to save file at: "{destination}", Error: {str(e)}')
        finally:
            file.file.close()


# validate images files
def validate_image_files(files=[]):
    try:
        for file in files:
            if file.content_type not in ALLOWED_IMAGE_TYPES:
                return False
        return True
    except Exception as e:
        raise Exception(f'Invalid image file, please check and try again. Error: {str(e)}')
