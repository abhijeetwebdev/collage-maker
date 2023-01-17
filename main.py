from config import PATHS
from services.collage_maker import CollageMaker

# image sources and dirs
uploads_dir = PATHS['UPLOADS']
target_image = f'{uploads_dir}/mario-tiny.jpg'
source_images = [
    f'{uploads_dir}/1.jpg',
    f'{uploads_dir}/2.jpg',
    f'{uploads_dir}/3.jpg',
    f'{uploads_dir}/4.jpg',
    f'{uploads_dir}/5.jpg'
]

# initiate and run collage maker
def main():
    collage_maker = CollageMaker()

    collage_maker.set_target_image(target_image)
    collage_maker.set_source_images(source_images)
    collage_maker.generate()

if __name__=='__main__':
    main()
