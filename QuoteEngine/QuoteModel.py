"""Encapsulates body and author class attributes."""


##############################
# Coding
##############################
class QuoteModel:
    """Class delivers the quote text body and its author."""

    def __init__(self, body="", author=""):
        """Initialise the instance object."""
        self.body = body
        self.author = author

    def __str__(self):
        """Return a instance explanation."""
        return f'Text quote body is:\n{self.body},\nby author {self.author}'

    def __repr__(self):
        """Return the technical instance information."""
        return f'"{self.body}" - {self.author}'

