from config import PATHS
from services.collage_maker import CollageMaker

# source image and dir
uploads_dir = PATHS['UPLOADS']
src_image_file = f'{uploads_dir}/mario-tiny.jpg'

# initiate and run collage maker
def main():
    collage_maker = CollageMaker()

    collage_maker.set_source_image(src_image_file)
    collage_maker.read_source_image()

if __name__=='__main__':
    main()
