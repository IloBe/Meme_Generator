"""Ingestor class of docx document files."""

##############################
# Imports
##############################
from typing import List
from docx import Document

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


##############################
# Coding
##############################
class DocxIngestor(IngestorInterface):
    """
    Concrete child class of the IngestorInterface.

    It implements the parse() function for docx documents
    to read quote block and author name.

    For docx Document see:
    https://python-docx.readthedocs.io/en/latest/

    returns: List[QuoteModel]
    """

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the content of the given docx document.

        input:
        path: (str) path of the docx document
        raise exception if the doc type is wrong (not docx)

        returns: List[QuoteModel]; model list of quotes and author
        names created of each line of the document not being empty
        """
        if not cls.can_ingest(path):
            raise Exception(f'DocxIngestor: cannot ingest file {path}')

        quote_models = []
        doc = Document(path)

        for paragraph in doc.paragraphs:
            if paragraph.text != "":
                # note: in the Word doc quote words are surrounded by ""
                # followed by ' - ' and the author name;
                # with doc content we define a new quote model for each line
                parse = paragraph.text.split(' - ')

                # all elements are strings: quote block, author name
                new_quote = QuoteModel(parse[0].replace('"', ''), parse[1])
                quote_models.append(new_quote)

        return quote_models
