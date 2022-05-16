""" ImageIngestor interface for images as abstract class """

##############################
# Imports
##############################
import logging
import pathlib
from abc import ABC, abstractmethod


##############################
# Coding
##############################
class ImageIngestorInterface(ABC):
    """
    ImageIngestorInterface implements the following methods:
        - can_ingest class method  -> boolean: to decide if a
          compatible image ingestor file exists
        - modify_image abstract class method: signature
          that must be realised in children classes of this interface
        """
    LOGGER = logging.getLogger(__name__)
    PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
    PROJECT_PHOTOS = PROJECT_ROOT / '_data' / 'photos'

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path) -> bool:
        """ Check the correct image type for meme creation """
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def modify_image(cls, img_path: str, width: int) -> str:
        """ Preprocessing of image """
