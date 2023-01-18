from PIL import Image, ImageEnhance
from config import CONFIG, PATHS
import random


class CollageMaker:

    def __init__(self):
        self.target_image = None
        self.target_image_ref = None
        self.source_images = None
        self.source_images_ref = None
        self.pixel_matrix = None
        self.collage_image = None
        self.uploads_dir = PATHS['UPLOADS']
        self.collages_dir = PATHS['COLLAGES']
        self.pixel_image_size = CONFIG['PIXEL_IMAGE_SIZE']
        self.pixel_image_opacity = CONFIG['PIXEL_IMAGE_OPACITY']


    # set source image link
    def set_target_image(self, url):
        self.target_image = f'{self.uploads_dir}/{url}'
        self.target_image_ref = Image.open(self.target_image)
        self.read_target_image()


    # get source image link
    def get_target_image(self):
        return self.target_image


    # read source image pixels data
    def read_target_image(self):
        image_data = list(self.target_image_ref.getdata())
        width, height = self.target_image_ref.size
        
        self.pixel_matrix = [image_data[i * width:(i + 1) * width] for i in range(height)]
        return self.pixel_matrix


    # set source image link
    def set_source_images(self, urls):
        self.source_images = urls
        self.source_images_ref = []
        for url in urls:
            source_image = f'{self.uploads_dir}/{url}'
            source_image = Image.open(source_image)
            source_image = self.crop_image_center(source_image)
            self.source_images_ref.append(source_image)


    # add small image the color tint of target image pixel
    def add_image_overlay(self, src, color='#FFFFFF', alpha=0.5):
        overlay = Image.new(src.mode, src.size, color)
        bw_src = ImageEnhance.Color(src).enhance(0.0)
        return Image.blend(bw_src, overlay, alpha)


    # convert rgb color to hex code
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb


    # crop image center, center
    def crop_image_center(self, img):
        width, height = img.size
        crop_width = min(img.size)
        crop_height = min(img.size)
        return img.crop(((width - crop_width) // 2, (height - crop_height) // 2, (width + crop_width) // 2, (height + crop_height) // 2))


    # start making collage image
    def generate(self):
        width, height = self.target_image_ref.size
        self.collage_image = Image.new(mode='RGB', size=(width*self.pixel_image_size, height*self.pixel_image_size))
        
        x_offset = 0
        y_offset = 0
        for row in self.pixel_matrix:
            for pixel in row:
                
                # get random image from the source images
                rand_index = random.randrange(4)
                pixel_image = self.source_images_ref[rand_index]
                
                # resize small image based on the pixel image size
                pixel_image_size = self.pixel_image_size, self.pixel_image_size
                pixel_image.thumbnail(pixel_image_size, Image.Resampling.LANCZOS)
                
                # add overlay color
                pixel_image = self.add_image_overlay(pixel_image, self.rgb_to_hex(pixel), self.pixel_image_opacity)
                
                # merge image to the specified position
                self.collage_image.paste(pixel_image, (x_offset, y_offset))
                
                # update x, y pointers
                x_offset += self.pixel_image_size
                if (x_offset >= self.collage_image.size[0]):
                    x_offset = 0
                    y_offset += self.pixel_image_size
        
        # save image
        self.collage_image.save(f'{self.collages_dir}/collage.png', 'PNG')
