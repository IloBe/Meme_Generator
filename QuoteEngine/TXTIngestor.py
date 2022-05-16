""" Ingestor class of txt document files """

##############################
# Imports
##############################
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


##############################
# Coding
##############################
class TXTIngestor(IngestorInterface):
    """
    Concrete child class of IngestorInterface,
    implementing the parse() function for txt documents
    to read quote block and author name.

    returns: List[QuoteModel]
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        '''
        Parses the content of the given txt document including
        a body and author column values separated by comma.

        input:
        path: (str) path of the txt document
        raise exception if the doc type is wrong (not txt)

        returns: List[QuoteModel]; model list of quotes and author
        names created of each line of the document
        '''
        if not cls.can_ingest(path):
            raise Exception(f'CSVIngestor: cannot ingest file {path}')

        quote_models = []

        with open(path, "r", encoding="utf-8-sig") as file_input:
            # Reading form a file line by line
            lines = file_input.readlines()
            for line in lines:
                # do line preprocessing for clean up,
                # remove extra spacing
                line = line.strip('\n\r').strip()
                if len(line) > 0:
                    # all elements are strings: quote block, author name
                    # quote body may be surrounded by ""
                    parse = line.replace('"', '').split(' - ')
                    new_quote = QuoteModel(parse[0], parse[1])
                    quote_models.append(new_quote)

        return quote_models
