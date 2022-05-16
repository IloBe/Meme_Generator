""" Ingestor interface for quote text bodies as abstract class """

##############################
# Imports
##############################
from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel


##############################
# Coding
##############################
class IngestorInterface(ABC):
    """
    IngestorInterface implements the following methods:
        - can_ingest class method  -> boolean: to decide if a
          compatible ingestor file exists
        - parse abstract class method -> List[QuoteModel]: signature
          that must be realised in children classes of this interface
        """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path) -> bool:
        """ Check the correct document type for meme creation """
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """ Parse the document """
