"""General image ingestor class to encapsulate specific helper classes."""

##############################
# Imports
##############################
import pathlib

from .ImageIngestorInterface import ImageIngestorInterface
from .JPGImageIngestor import JPGImageIngestor
from .PNGImageIngestor import PNGImageIngestor


##############################
# Coding
##############################
class ImageIngestor(ImageIngestorInterface):
    """
    Factory to select and return the specific ImageIngestor class.

    Function modify_imge() result depends on file type extension.

    Allowed are jpg, jpeg and png images.
    The png images we are using are from:
    https://www.freepngs.com/animal-pngs
    """

    @classmethod
    def in_extension(cls, ext: str) -> bool:
        """
        Check if the extension is in valid extension list.

        Valid types are .jpg, .jpeg and .png.

        input:
        ext: (str) given image extension

        return: Boolean value if ext in extension or not
        """
        img_ext = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG', '.webp', '.WEBP']
        return ext in img_ext

    @classmethod
    def modify_image(cls, img_path: str, width: int) -> str:
        """
        Encapsulate the specific ImageIngestor helper classes.

        Their modification result is based on given image type.

        input:
        img_path: (str) specific image and its path information
        Raises a ValueError, if a wrong extension is given.

        Return: Path of the modified image storage
        """
        cls.LOGGER.info(f'ImageIngestor: image path to modify: {img_path}')
        preproc_path = ''
        img_ext = pathlib.Path(img_path).suffix
        if not cls.in_extension(img_ext):
            cls.LOGGER.error(
                f'Wrong image type, throws ValueError; img_ext: "{img_ext}"')
            raise ValueError(f'ImageIngestor: wrong extension {img_ext}')

        if img_ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
            preproc_path = JPGImageIngestor.modify_image(img_path, width)
        if img_ext in ['.png', '.PNG']:
            preproc_path = PNGImageIngestor.modify_image(img_path, width)
        if img_ext in ['.webp', '.WEBP']:
            # use jpg ingestor not having a grayscale transformation as it
            # is implemented for png images with png ingestor instance
            preproc_path = JPGImageIngestor.modify_image(img_path, width)

        return preproc_path
