from services.collage_maker import CollageMaker

# image sources and dirs
target_image = 'mario-small.jpg'
source_images = [
    '1.png',
    '2.jpg',
    '3.jpg',
    '4.jpg',
    '5.jpg'
]

# initiate and run collage maker
def main():
    collage_maker = CollageMaker()

    collage_maker.set_target_image(target_image)
    collage_maker.set_source_images(source_images)
    collage_maker.generate()

if __name__=='__main__':
    main()
