#!/usr/bin/env python3

"""
This Flask app uses the implemented modules
- 'QuoteEngine' and
- 'MemeGenerator'
to create a random captioned meme image
or a user customised one.
"""

##############################
# Imports
##############################
import random
import os
import shutil
import requests
from flask import Flask, render_template, request

from QuoteEngine.Ingestor import Ingestor
from MemeGenerator import MemeEngine


##############################
# Coding
##############################
app = Flask(__name__)
STATIC_DIR = './static'
if os.path.exists(STATIC_DIR):
    shutil.rmtree(STATIC_DIR)
meme = MemeEngine(STATIC_DIR)


def setup():
    """ Load all resources """

    # quotes ...
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    try:
        for quote_file in quote_files:
            quotes.extend(Ingestor.parse(quote_file))
    except (ValueError, FileNotFoundError) as err:
        print(f'Flask app setup(): ValueError, FileNotFoundError: {err}')

    # images ...
	# Use the pythons standard library os class to find all
    # images within the images images_path directory
	# jpg images
    images_path = "./_data/photos/dog/"
    imgs = []
    imgs_wolf = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    # png images
    images_path = "./_data/photos/wolf/"
    for root, dirs, files in os.walk(images_path):
        imgs_wolf = [os.path.join(root, name) for name in files]
    # put all images in one list
    imgs.extend(imgs_wolf)

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme as .jpg image """

    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form parameters.
    # 3. Remove the temporary saved image.

    # param names are in meme_form.html of templates dir
    local_img = './tmp/local_img.jpg'
    image_url = request.form.get('image_url')
    img_file = requests.get(image_url, stream=True).content
    with open(local_img, "wb") as in_file:
        in_file.write(img_file)

    body = request.form.get('body', '')
    author = request.form.get('author', '')
    path = meme.make_meme(local_img, body, author)
    print(f'Flask app meme_post(): image path: {path}')
    os.remove(local_img)
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    # use this run command for testing only, not for production server,
	# because valid secure certificate is not created
    app.run(host='0.0.0.0', port=3001, ssl_context='adhoc', debug=True)
