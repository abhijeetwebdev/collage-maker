from PIL import Image, ImageEnhance
from config import CONFIG, PATHS
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
        self._collages_dir = PATHS['COLLAGES']
        self._pixel_image_size = CONFIG['PIXEL_IMAGE_SIZE']
        self._pixel_image_opacity = CONFIG['PIXEL_IMAGE_OPACITY']


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
        self._source_images_ref = []
        for url in urls:
            source_image = Image.open(url)
            source_image = self._crop_center(source_image)
            self._source_images_ref.append(source_image)


    # add small image the color tint of target image pixel
    def _image_overlay(self, src, color='#FFFFFF', alpha=0.5):
        overlay = Image.new(src.mode, src.size, color)
        bw_src = ImageEnhance.Color(src).enhance(0.0)
        return Image.blend(bw_src, overlay, alpha)


    # convert rgb color to hex code
    def _rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb


    # crop image center, center
    def _crop_center(self, img):
        width, height = img.size
        crop_width = min(img.size)
        crop_height = min(img.size)
        return img.crop(((width - crop_width) // 2, (height - crop_height) // 2, (width + crop_width) // 2, (height + crop_height) // 2))


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
                pixel_image = self._source_images_ref[rand_index]
                
                # resize small image based on the pixel image size
                pixel_image_size = self._pixel_image_size, self._pixel_image_size
                pixel_image.thumbnail(pixel_image_size, Image.Resampling.LANCZOS)
                
                # add overlay color
                pixel_image = self._image_overlay(pixel_image, self._rgb2hex(pixel), self._pixel_image_opacity)
                
                # merge image to the specified position
                self._collage_image.paste(pixel_image, (x_offset, y_offset))
                
                # update x, y pointers
                x_offset += self._pixel_image_size
                if (x_offset >= self._collage_image.size[0]):
                    x_offset = 0
                    y_offset += self._pixel_image_size
        
        # save image
        self._collage_image.save(f'{self._collages_dir}/collage.png', 'PNG')
