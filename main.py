from services.collage_maker import CollageMaker
from utils import helper
from config import PATHS
import logging

# setup logging
helper.setup_logging()

# image sources and dirs
target_image = 'car.jpg'
source_images = helper.get_images_from_dir(PATHS['UPLOADS'])

# initiate and run collage maker
def main():
    collage_maker = CollageMaker()
    collage_maker.set_target_image(target_image)
    collage_maker.set_source_images(source_images)
    collage_maker.generate()

if __name__=='__main__':
    try:
        main()
    except Exception as err:
        logging.error(str(err))
