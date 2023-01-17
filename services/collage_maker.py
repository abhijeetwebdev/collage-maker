from PIL import Image, ImageEnhance
from config import PATHS
import random


class CollageMaker:

    def __init__(self):
        self._target_image = None
        self._target_image_ref = None
        self._source_images = None
        self._source_images_ref = None
        self._pixel_matrix = None
        self._collage_image = None
        self._uploads_dir = PATHS['UPLOADS']
        self._pixel_image_size = 100


    # set source image link
    def set_target_image(self, url):
        self._target_image = url
        self._target_image_ref = Image.open(url)
        self._read_target_image()


    # get source image link
    def get_target_image(self):
        return self._target_image


    # read source image pixels data
    def _read_target_image(self):
        image_data = list(self._target_image_ref.getdata())
        width, height = self._target_image_ref.size
        
        self._pixel_matrix = [image_data[i * width:(i + 1) * width] for i in range(height)]
        return self._pixel_matrix


    # set source image link
    def set_source_images(self, urls):
        self._source_images = urls
        self._source_images_ref = [Image.open(u) for u in urls]


    # add small image the color tint of target image pixel
    def _image_overlay(self, src, color='#FFFFFF', alpha=0.5):
        overlay = Image.new(src.mode, src.size, color)
        bw_src = ImageEnhance.Color(src).enhance(0.0)
        return Image.blend(bw_src, overlay, alpha)


    # convert rgb color to hex code
    def _rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb


    # start making collage image
    def generate(self):
        width, height = self._target_image_ref.size
        self._collage_image = Image.new(mode='RGB', size=(width*self._pixel_image_size, height*self._pixel_image_size))
        
        x_offset = 0
        y_offset = 0
        for row in self._pixel_matrix:
            for pixel in row:
                
                # get random image from the source images
                rand_index = random.randrange(4)
                temp_image = self._source_images_ref[rand_index]
                
                # add overlay color
                temp_image = self._image_overlay(temp_image, self._rgb2hex(pixel))
                
                # merge image to the specified position
                self._collage_image.paste(temp_image, (x_offset, y_offset))
                
                # update x, y pointers
                x_offset += self._pixel_image_size
                if (x_offset >= self._collage_image.size[0]):
                    x_offset = 0
                    y_offset += self._pixel_image_size
        
        # save image
        self._collage_image.save(f'{self._uploads_dir}/collage.png', 'PNG')
