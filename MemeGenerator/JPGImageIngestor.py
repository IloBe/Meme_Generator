"""ImageIngestor class of jpg/jpeg image files."""

##############################
# Imports
##############################
import pathlib
from PIL import Image

from .ImageIngestorInterface import ImageIngestorInterface


##############################
# Coding
##############################
class JPGImageIngestor(ImageIngestorInterface):
    """
    Concrete child class of the ImageIngestorInterface.

    This class handles jpg images.
    """

    allowed_extensions = ['jpg', 'jpeg', 'JPEG', 'JPG', 'webp', 'WEBP']

    def __str__(self):
        """Return JPGImageIngestor class information."""
        return 'JPGImageIngestor child class of ImageIngestorInterface.'

    @classmethod
    def modify_image(cls, img_path, width=500) -> str:
        """
        Preprocessing of image; being a jpg image, scaling is done.

        input:
        img_path: (str) path of image used for preprocessing
        width: (int) width value for scaling, preserves aspect ration

        return: path string of preprocessed image
        """
        img_ext = pathlib.Path(img_path).suffix  # image extension
        print(f'===> JPG ingestor: img ext: {img_ext}')
        if not cls.can_ingest(img_ext):
            cls.LOGGER.error(f'Wrong image type to create meme: {img_path}')
            raise Exception(f'JPGImageIngestor cannot ingest image {img_path}')

        save_path = cls.PROJECT_PHOTOS
        img_parent = pathlib.Path(img_path).parent
        img_name = pathlib.Path(img_path).name
        cls.LOGGER.info(
            f'JPG ingestor: img_parent: {img_parent}, img_name: {img_name}')

        try:
            with Image.open(img_path) as in_img:
                cls.LOGGER.info(f'orig image size: {in_img.size}')
                print(f'orig image size: {in_img.size}')
                # create a new image and preserve aspect ratio
                if in_img.size[0] > 500:
                    width = 500
                else:
                    width = in_img.size[0]
                new_height = int(width*in_img.size[1] / float(in_img.size[0]))
                new_size = (width, new_height)
                in_img = in_img.resize(new_size, Image.ANTIALIAS)
                # in_img.show() # only for testing
                cls.LOGGER.info(f'New mod image size: {in_img.size}')

                # convert webp to jpg format if necessary before saving
                if img_ext in ['.webp', '.WEBP']:
                    in_img = in_img.convert('RGB')
                    img_name = img_name.lower().removesuffix('.webp') + '.jpg'

                save_path = pathlib.Path.joinpath(img_parent, 'mod_'+img_name)
                # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
                in_img.save(save_path, format='jpeg')
        except (OSError, FileNotFoundError) as err:
            cls.LOGGER.error(f'Error to create/save modified image:\n +\
                        error message: {err}')
            print(f'JPGImageIngestor cannot create/save modified {img_path}')
            raise

        cls.LOGGER.info(f'Modified image path for meme creation: {save_path}')
        return str(save_path)
