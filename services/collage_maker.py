from PIL import Image, ImageEnhance
from config import CONFIG, PATHS
import random


class CollageMaker:

    def __init__(self):
        self.target_img_name = None
        self.target_img = None
        self.src_img_names = None
        self.src_imgs = None
        self.pixel_matrix = None
        self.collage_img = None
        self.uploads_dir = PATHS['UPLOADS']
        self.collages_dir = PATHS['COLLAGES']
        self.pixel_img_size = CONFIG['PIXEL_IMAGE_SIZE']
        self.pixel_img_opacity = CONFIG['PIXEL_IMAGE_OPACITY']


    # set source image link
    def set_target_image(self, img_name):
        self.target_img_name = img_name
        self.target_img = Image.open(f'{self.uploads_dir}/{img_name}')
        self.read_target_image()


    # set source image link
    def set_source_images(self, names):
        self.src_img_names = names
        self.src_imgs = []
        for img_name in names:
            src_img = f'{self.uploads_dir}/{img_name}'
            src_img = Image.open(src_img)
            src_img = self.crop_image_center(src_img)
            self.src_imgs.append(src_img)


    # read source image pixels data
    def read_target_image(self):
        img_data = list(self.target_img.getdata())
        width, height = self.target_img.size
        self.pixel_matrix = [img_data[i * width:(i + 1) * width] for i in range(height)]
        return self.pixel_matrix


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
        width, height = self.target_img.size
        self.collage_img = Image.new(mode='RGB', size=(width*self.pixel_img_size, height*self.pixel_img_size))
        
        x_offset = 0
        y_offset = 0
        for row in self.pixel_matrix:
            for pixel in row:
                
                # get random image from the source images
                rand_index = random.randrange(4)
                pixel_img = self.src_imgs[rand_index]
                
                # resize small image based on the pixel image size
                pixel_img_size = self.pixel_img_size, self.pixel_img_size
                pixel_img.thumbnail(pixel_img_size, Image.Resampling.LANCZOS)
                
                # add overlay color
                pixel_img = self.add_image_overlay(pixel_img, self.rgb_to_hex(pixel), self.pixel_img_opacity)
                
                # merge image to the specified position
                self.collage_img.paste(pixel_img, (x_offset, y_offset))
                
                # update x, y pointers
                x_offset += self.pixel_img_size
                if (x_offset >= self.collage_img.size[0]):
                    x_offset = 0
                    y_offset += self.pixel_img_size
        
        # save image
        self.collage_img.save(f'{self.collages_dir}/{self.target_img_name}')
