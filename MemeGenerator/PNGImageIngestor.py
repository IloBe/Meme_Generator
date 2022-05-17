""" ImageIngestor class of png image files """

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
    Concrete child class of the ImageIngestorInterface
	PNG images are modified being grayscale images at the end.
	Therefore modes concept of Pillow is used:
	https://pillow.readthedocs.io/en/stable/handbook/concepts.html?highlight=bands#modes
    """

    allowed_extensions = ['png', 'PNG']

    def __str__(self):
        return 'PNGImageIngestor child class of ImageIngestorInterface.'


    @classmethod
    def modify_image(cls, img_path, width) -> str:
        img_ext = pathlib.Path(img_path).suffix
        if not cls.can_ingest(img_ext):
            cls.LOGGER.error(f'Wrong image type is given to create the meme: {img_path}')
            raise Exception(f'PNGImageIngestor: cannot ingest image {img_path}')

        img_parent = pathlib.Path(img_path).parent
        img_name = pathlib.Path(img_path).name
        save_path = cls.PROJECT_PHOTOS
        cls.LOGGER.info(f'PNGImageIngestor: img_parent: {img_parent}, img_name: {img_name}')

        # for image scaling, image shall not be too small or too big
        if width < 50 or width > 500:
            cls.LOGGER.info('Not acceptable range of width: 50 - 500; so set to 500.')
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
                new_height = int(width * in_img.size[1] / float(in_img.size[0]))
                new_size = (width, new_height)
                in_img = in_img.resize(new_size, Image.ANTIALIAS)
                #in_img.show()  # for testing only
                print(f'mod image size: {in_img.size}')
                cls.LOGGER.info(f'New mod image size: {in_img.size}')
                #print(f'original image bands shall be RGB: {in_img.getbands()}')

                # create grayscale image
                gray_img = in_img.convert("L")
                #gray_img.show()  # for testing only
                print(f'converted image bands shall be L for grayscale: {gray_img.getbands()}')

                save_path = pathlib.Path.joinpath(img_parent, 'mod_'+img_name)
                gray_img.save(save_path, format='png')
        except (OSError, FileNotFoundError) as err:
            cls.LOGGER.error(f'Error to create/save modified image {img_path}, err: {err}')
            print(f'PNGImageIngestor: cannot create/save modified grayscale image of {img_path}')

        cls.LOGGER.info(f'Path of modified image for meme creation: {save_path}')
        return str(save_path)
