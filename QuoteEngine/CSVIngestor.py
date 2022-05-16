""" Ingestor class of csv document files """

##############################
# Imports
##############################
from typing import List
import pandas as pd

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


##############################
# Coding
##############################
class CSVIngestor(IngestorInterface):
    """
    Concrete child class of IngestorInterface,
    implementing the parse() function for csv documents
    to read quote block and author name.

    returns: List[QuoteModel]
    """
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        '''
        Parses the content of the given csv document including
        a body and author column values separated by comma.

        input:
        path: (str) path of the csv document
        raise exception if the doc type is wrong (not csv)

        returns: List[QuoteModel]; model list of quotes and author
        names created of each line of the document, except the header
        '''
        if not cls.can_ingest(path):
            raise Exception(f'CSVIngestor: cannot ingest file {path}')

        df_csv = pd.read_csv(path, header=0)
        quote_models = [QuoteModel(**row) for index, row in df_csv.iterrows()]

        return quote_models
