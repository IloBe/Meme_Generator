"""QuoteEngine package initialisation."""

###############
# Imports
###############
import logging
from datetime import datetime

from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface
from .DocxIngestor import DocxIngestor
from .CSVIngestor import CSVIngestor
from .TXTIngestor import TXTIngestor
from .PDFIngestor import PDFIngestor
from .Ingestor import Ingestor


###############
# Constants
###############
# Create current date string
STR_CURRENT_DATE = datetime.today().strftime('%Y-%m-%d')


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
