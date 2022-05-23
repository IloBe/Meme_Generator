"""MemeGenerator package initialisation."""

###############
# Imports
###############
import logging
import pathlib
from datetime import datetime

from .ImageIngestorInterface import ImageIngestorInterface
from .JPGImageIngestor import JPGImageIngestor
from .PNGImageIngestor import PNGImageIngestor
from .ImageIngestor import ImageIngestor
from .MemeEngine import MemeEngine

###############
# Constants
###############

# Create current date string
STR_CURRENT_DATE = datetime.today().strftime('%Y-%m-%d')

# Paths to the root of the project, containing the main.py file
PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
PROJECT_PHOTOS = PROJECT_ROOT / '_data' / 'photos'
PROJECT_PHOTOS_DOG = PROJECT_PHOTOS / 'dog'
PROJECT_PHOTOS_WOLF = PROJECT_PHOTOS / 'wolf'
SAVE_IMAGE_PATH = PROJECT_ROOT / 'tmp'

###############
# Coding
###############

# Logging concept: simple logging with root logger
# see:
# https://docs.python.org/3/howto/logging.html#displaying-the-date-time-in-messages


def config_basic_root_logger():
    """Configure log format for root logger, append messages to log file."""
    logging.basicConfig(
        filename='./logs/meme_project_' + STR_CURRENT_DATE + '.log',
        level=logging.DEBUG,  # future toDo: could be set with CLI argument
        filemode='a',
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    )


def get_logger():
    """Return the root logger."""
    return logging.getLogger()


config_basic_root_logger()
LOGGER = get_logger()
