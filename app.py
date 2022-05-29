#!/usr/bin/env python3

"""
Script to start the meme generator via simple Flask browser app.

This Flask app uses the implemented modules
- 'QuoteEngine' and
- 'MemeGenerator'
to create a random captioned meme image
or a user customised one, which is overwritten by creating a new one.

Regarding text wrapping, there is still a little mistake during creation
of own text bodies (see: https://docs.python.org/3/library/textwrap.html):
If a word is too long for font depending text bounding box, the text
wrapper instance breaks it down into few parts, fitting to availabe
position area. The separation might not fit to spelling.

Regarding the customised creation of a meme image by an app user,
they have to take care of the image type extension for the given URL.
It should be one of the following:
- .png, .PNG, .jpg, .JPG, .jpeg, .JPEG, .webp, .WEBP

WEBP resp. webp photos are converted to RGB .jpg images, so, the app can
handle them.
For all other URL strings given by a user a FileNotFoundError is thrown.
You will see random and create Buttons with a broken image icon on the
browser page. The buttons are still active for a new choise.

To handle Flask exceptions, coding is based on reading this blogs:
https://flask.palletsprojects.com/en/2.1.x/errorhandling/?highlight=exceptionsc
or https://opensource.com/article/17/3/python-flask-exceptions.
How to handle associated customer error pages is described e.g. on page:
https://www.digitalocean.com/community/tutorials/how-to-handle-errors-in-a-flask-application
"""

##############################
# Imports
##############################
import random
import os
import pathlib
import shutil
import requests
from flask import Flask, render_template, request, abort
from werkzeug.utils import secure_filename

from QuoteEngine.Ingestor import Ingestor
from MemeGenerator import MemeEngine
from app import get_app_instance


##############################
# Coding
##############################
app = get_app_instance()

STATIC_DIR = './static'
if os.path.exists(STATIC_DIR):
    shutil.rmtree(STATIC_DIR)
meme = MemeEngine(STATIC_DIR)


def setup():
    """Load all resources."""
    app.logger.info('Flask meme app: Load all resources...')
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
    """Generate a random meme."""
    app.logger.info('Generate a random meme.')
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    print(f'Flask app meme_rand(): path of make_meme: {path}')
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme as .jpg or .png image."""
    app.logger.info('Create a user defined meme as .jpg or .png.')
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form parameters.
    # 3. Remove the temporary saved image.

    # param names are in meme_form.html of templates dir
    url = request.form.get('image_url')
    secure_url = url.strip('https://')
    secure_url = secure_filename(secure_url)
    app.logger.debug(f'Passed check if URL is secure: {secure_url}')
    secure_url = 'https://' + secure_url

    # image type detection can be changed to strategy pattern as well
    try:
        app.logger.debug(f'Imge type detection for URL: {url}')
        img_ext = pathlib.Path(secure_url).suffix
        if img_ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
            local_img = './tmp/local_app_img.jpg'
        elif img_ext in ['.png', '.PNG']:
            local_img = './tmp/local_app_img.png'
        elif img_ext in ['.webp', '.WEBP']:
            local_img = './tmp/local_app_img.webp'
        else:
            # no extention given, create a default jpg image
            print(f'Flask /create: wrong .jpg,.png,.webp URL: {url}')
            print(f'==> img_ext is:{img_ext}')
            print('==> we transform it to .jpg image')
            if len(url) > 0:
                url = url + '.jpg'
                local_img = './tmp/local_app_img.jpg'
    except TypeError as err:
        print('Flask app meme post abort 404, no valid image type given ...')
        app.logger.error('Flask app post abort 404 no valid image type given')
        abort(404)

    try:
        app.logger.debug('Get image content ...')
        img_file = requests.get(url, stream=True).content
        if img_file is None:
            print('No valid image URL to get image bytes object is given.')
            print('Flask app post abort 404, no valid image file content ...')
            app.logger.warning('No valid image content could be get ...')
            abort(404)

        with open(local_img, "wb") as in_file:
            in_file.write(img_file)

        body = request.form.get('body', '')
        author = request.form.get('author', '')
        print('Flask app /create meme post() calls make_meme()')
        path = meme.make_meme(local_img, body, author)
        print(f'Flask app /create meme_post(): image path: {path}')
        os.remove(local_img)
        return render_template('meme.html', path=path)

    except Exception as exc:
        print(f'Flask app /create meme_post: exception: {exc}')
        print('Flask app abort 404, end of post create ...')
        app.logger.error(f'Flask app /create meme_post: exception: {exc}')
        abort(404)


if __name__ == "__main__":
    # use this run command for development only, not for production server,
    # because valid secure certificate is not created;
    # for public repo: debug mode is set to False, avoid security risk
    app.run(host='0.0.0.0', port=3001, ssl_context='adhoc', debug=False)
