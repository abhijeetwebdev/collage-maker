from config import PATHS
from services.collage_maker import CollageMaker

# source image and dir
uploads_dir = PATHS['UPLOADS']
target_image = f'{uploads_dir}/mario-tiny.jpg'
source_images = []

# initiate and run collage maker
def main():
    collage_maker = CollageMaker()

    collage_maker.set_target_image(target_image)
    collage_maker.read_target_image()
    # collage_maker.set_source_images()

if __name__=='__main__':
    main()
