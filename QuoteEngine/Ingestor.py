""" General Ingestor class to encapsulate the specific helper classes """

##############################
# Imports
##############################
import pathlib
from typing import List

from .IngestorInterface import IngestorInterface
from .DocxIngestor import DocxIngestor
from .CSVIngestor import CSVIngestor
from .TXTIngestor import TXTIngestor
from .PDFIngestor import PDFIngestor
from .QuoteModel import QuoteModel


##############################
# Coding
##############################
class Ingestor(IngestorInterface):
    """
    Factory to select and return the specific Ingestor class,
    parsing result depends on file type extension.
    """

    @classmethod
    def in_extension(cls, ext) -> bool:
        """
        Check if the valid document extension exits.
        Valid are .docx, .csv, .txt and .pdf.

        input:
        ext: (str) document extension

		return: True or False depending if ext param is in valid list
        """
        file_ext = ['.docx', '.csv', '.txt', '.pdf']
        return ext in file_ext

    @classmethod
    def parse(cls, path) -> List[QuoteModel]:
        """
        Encapsulates the specific Ingestor helper classes and
        their parse result based on given file type.

        input:
        path: (str) specific file and its path information
        Raises a ValueError, if a wrong extension is given.

        Return: (List[QuoteModel]) specific Ingestor class parse result
        """
        doc_path = ''
        file_extension = pathlib.Path(path).suffix
        if not cls.in_extension(file_extension):
            cls.LOGGER.error(
                'Wrong document type, therefore a ValueError is thrown.')
            raise ValueError(f'Ingestor: wrong extension {file_extension}')

        if file_extension == '.docx':
            doc_path = DocxIngestor.parse(path)
        if file_extension == '.csv':
            doc_path = CSVIngestor.parse(path)
        if file_extension == '.txt':
            doc_path = TXTIngestor.parse(path)
        if file_extension == '.pdf':
            doc_path = PDFIngestor.parse(path)

        return doc_path
