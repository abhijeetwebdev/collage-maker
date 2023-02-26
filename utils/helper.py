import os
import cv2
import logging

# setup logging
def setup_logging():
    logging.basicConfig(
        filename = './storage/collage-maker.log',
        format = '%(levelname) -10s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s',
        level = logging.INFO
    )


# get the list of source images from uploads dir
def get_images_from_dir(dir):
    img_names = []
    for filename in os.listdir(dir):
        img = cv2.imread(os.path.join(dir, filename))
        if img is not None:
            img_names.append(filename)
    return img_names
