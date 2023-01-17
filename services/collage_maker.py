from PIL import Image, ImageOps


class CollageMaker:

    def __init__(self):
        self._target_image_url = None
        self._target_image_ref = None
        self._pixel_matrix = None
        self._source_image_urls = None


    # set source image link
    def set_target_image(self, url):
        self._target_image_url = url
        self._target_image_ref = Image.open(url)
        self._read_target_image()


    # get source image link
    def get_target_image(self):
        return self._target_image_url


    # read source image pixels data
    def _read_target_image(self):
        image_data = list(self._target_image_ref.getdata())
        width, height = self._target_image_ref.size
        
        self._pixel_matrix = [image_data[i * width:(i + 1) * width] for i in range(height)]
        return self._pixel_matrix


    # set source image link
    def set_source_images(self, urls):
        self._source_image_urls = urls

    
    def generate(self):
        print('Start generating collage image')
        
