"""ImageIngestor class of png image files."""

##############################
# Imports
##############################
import pathlib
from PIL import Image

from .ImageIngestorInterface import ImageIngestorInterface


##############################
# Coding
##############################
class PNGImageIngestor(ImageIngestorInterface):
    """
    Concrete child class of the ImageIngestorInterface.

    PNG images are modified being grayscale images at the end.
    Therefore modes concept of Pillow is used:
    https://pillow.readthedocs.io/en/stable/handbook/concepts.html?highlight=bands#modes
    """

    allowed_extensions = ['png', 'PNG']

    def __str__(self):
        """Return PNGImageIngestor class information."""
        return 'PNGImageIngestor child class of ImageIngestorInterface.'

    @classmethod
    def modify_image(cls, img_path, width) -> str:
        """
        Preprocessing of image; being a png image,.

        Having a png image, scaling and grayscale transformation is done.

        input:
        img_path: (str) path of image used for preprocessing
        width: (int) width value for scaling, preserves aspect ration

        return: path string of preprocessed image
        """
        img_ext = pathlib.Path(img_path).suffix
        if not cls.can_ingest(img_ext):
            cls.LOGGER.error(f'Wrong image type given for meme: {img_path}')
            raise Exception(f'PNG ingestor cannot ingest image {img_path}')

        img_parent = pathlib.Path(img_path).parent
        img_name = pathlib.Path(img_path).name
        save_path = cls.PROJECT_PHOTOS
        cls.LOGGER.info('PNGImageIngestor')
        cls.LOGGER.info(f'-img_parent: {img_parent},\n- img_name: {img_name}')

        # for image scaling, image shall not be too small or too big
        if width < 50 or width > 500:
            cls.LOGGER.info('Not acceptable width range 50 - 500; set to 500')
            width = 500

        try:
            with Image.open(img_path) as in_img:
                cls.LOGGER.info(f'orig image size: {in_img.size}')
                print(f'orig image size: {in_img.size}')
                # create a new image and preserve aspect ratio, resize height
                if in_img.size[0] > 500:
                    width = 500
                else:
                    width = in_img.size[0]
                new_height = int(width*in_img.size[1] / float(in_img.size[0]))
                new_size = (width, new_height)
                in_img = in_img.resize(new_size, Image.ANTIALIAS)
                # in_img.show() # only for testing
                cls.LOGGER.info(f'New mod image size: {in_img.size}')

                # create grayscale image
                gray_img = in_img.convert("L")
                # only for testing
                # gray_img.show()
                print(f'converted img is L grayscale: {gray_img.getbands()}')

                save_path = pathlib.Path.joinpath(img_parent, 'mod_'+img_name)
                gray_img.save(save_path, format='png')
        except (OSError, FileNotFoundError) as err:
            cls.LOGGER.error(f'Error on modified png {img_path}, err: {err}')

        cls.LOGGER.info(f'Modified image path for meme creation: {save_path}')
        return str(save_path)
