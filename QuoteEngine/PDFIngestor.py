""" Ingestor class of pdf document files """

##############################
# Imports
##############################
from typing import List
import subprocess
import os
import random

from .IngestorInterface import IngestorInterface
from .TXTIngestor import TXTIngestor
from .QuoteModel import QuoteModel


##############################
# Coding
##############################
class PDFIngestor(IngestorInterface):
    """
    Concrete child class of IngestorInterface,
    implementing the parse() function for pdf documents
    to read quote block and author name.

    returns: List[QuoteModel]
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception(f'PDFIngestor: cannot ingest file {path}')

        # create random name for our text file
        tmp = f'./tmp/{random.randint(0,10000000)}.txt'

        # call CLI tool pdftotext from xpdf library, input path, output file
        try:
            subprocess.call(['pdftotext', path, tmp])
        except OSError as err:
            raise Exception('PDFIngestor: no subprocess pdftotext call' +
                            f'for output file {tmp}; error: {err}')

        # we work with that txt file and get the QuoteModel instances
        quote_models = TXTIngestor.parse(tmp)

        # remove the tmp file from disk
        os.remove(tmp)

        return quote_models
