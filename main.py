#!/usr/bin/env python3
"""
Create meme images from given images, text quote bodies and author.
You can assign specific image and quote via own argument information.

So, this script can be invoked from the command line with and without
arguments. If no argument is given, a random meme is created. By
using your own arguments for --body and --author put double quotes
around them to handle string sentences and have in mind that they
always belong together.
    $ python3 main.py [args] with args being --path, --body, --author

Note: Another option to create meme images are the usage of the
Flask app.py script delivered with this project.
"""

##############################
# Imports
##############################

import argparse
import os
import random
import traceback

from QuoteEngine.Ingestor import Ingestor
from QuoteEngine.QuoteModel import QuoteModel
from MemeGenerator import MemeEngine


##############################
# Coding
##############################


def generate_meme(path=None, body=None, author=None) -> str:
    """
    Generate a meme given an imge path, a quote and the quotes author.

    input:
    path: (str) path of the image used to create the meme
    body: (str) text used for the meme
    author: (str) author of the given meme text

    return: path string of the created meme
    """
    img = None
    quote = None

    try:
        if path is None:
            # jpg images
            images = "./_data/photos/dog/"
            imgs = []
            imgs_wolf = []
            for root, dirs, files in os.walk(images):
                print(f'for path argument, dog:\n- root: {root}\n- dirs: {dirs}\n- files: {files}')
                imgs = [os.path.join(root, name) for name in files]

            # png images
            images = "./_data/photos/wolf/"
            for root, dirs, files in os.walk(images):
                print(f'for path argument, wolf:\n- root: {root}\n- dirs: {dirs}\n- files: {files}')
                imgs_wolf = [os.path.join(root, name) for name in files]

            imgs.extend(imgs_wolf)
            img = random.choice(imgs)
        else:
            img = path

        if body is None:
            if author is not None:
                raise Exception('Body required if author param is used')

            quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                           './_data/DogQuotes/DogQuotesDOCX.docx',
                           './_data/DogQuotes/DogQuotesPDF.pdf',
                           './_data/DogQuotes/DogQuotesCSV.csv']
            quotes = []
            for quote_file in quote_files:
                quotes.extend(Ingestor.parse(quote_file))
            quote = random.choice(quotes)	
        else:
            if author is None:
                raise Exception('Author required if body param is used')
            quote = QuoteModel(body, author)

        meme = MemeEngine('./tmp')
        print(f'Main call: Create meme with quote: {quote}')
        path = meme.make_meme(img, quote.body, quote.author)
    except Exception as err:
        print(f'Raised exception type: {type(err)}; its traceback is:')
        traceback.print_tb(err.__traceback__)

    return path


if __name__ == "__main__":
    # Use ArgumentParser to parse the following CLI arguments:
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image

    parser = argparse.ArgumentParser(
        description="Meme image & text defined by user. Meme path printed.")

    # Add arguments for custom data files.
    parser.add_argument('--path', default=None,
                        type=str, required=False,
                        help="Path of basic image file used for meme.")
    parser.add_argument('--body', default=None,
                        type=str, required=False,
                        help="Quote text body to add to the image.")
    parser.add_argument('--author', default=None,
                        type=str, required=False,
                        help="Quote body author to add to the image.")

    args = parser.parse_args()
    print('Your CLI arguments are:')
    print(f'- args.path: "{args.path}"')
    print(f'- args.body: "{args.body}"')
    print(f'- args.author: "{args.author}"')
    final_path = generate_meme(args.path, args.body, args.author)
    msg = "No meme created because of wrong arguments"
    print(f'Path of created meme: {msg if final_path is None else final_path}')
