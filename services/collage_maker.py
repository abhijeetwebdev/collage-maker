from PIL import Image, ImageOps


class CollageMaker:

    def __init__(self):
        self._source_image_url = None
        self._source_image_ref = None
        self._pixel_matrix = None
        self._target_image_url = None

    # set source image link
    def set_source_image(self, url):
        self._source_image_url = url
        self._source_image_ref = Image.open(url)
        
    # get source image link
    def get_source_image(self):
        return self._source_image_url
    
    # read source image pixels data
    def read_source_image(self):
        src_data = list(self._source_image_ref.getdata())
        width, height = self._source_image_ref.size
        print('src_data START')
        print(src_data)
        print('src_data END')
        self._pixel_matrix = [src_data[i * width:(i + 1) * width] for i in range(height)]
        print('pixel_matrix')
        print(self._pixel_matrix)

