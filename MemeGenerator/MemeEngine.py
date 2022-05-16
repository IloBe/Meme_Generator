"""
Class to create and handle the meme images

Overview-tutorials about image handing and the used library Pillow:
https://realpython.com/image-processing-with-the-python-pillow-library/
or
https://machinelearningmastery.com/how-to-load-and-manipulate-images-for-deep-learning-in-python-with-pil-pillow/

The Pillow documentation is given with:
https://pillow.readthedocs.io/en/stable/reference/Image.html
or
https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#example-draw-multiline-text
or
https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
"""

##############################
# Imports
##############################
import os
import pathlib
import logging
import random
import PIL
from PIL import Image, ImageDraw, ImageFont

from .ImageIngestor import ImageIngestor

##############################
# Coding
##############################
class MemeEngine():
    """
    Handles the images by usage of pillow PIL library.
	It combines the quote text bodies with the image to
	show the final meme and stores it by default in tmp
	dir of the projects source directory.
    """

    def __init__(self, out_dir='../tmp'):
        print(f'==> MemeEngine: __init__: out_dir: {out_dir}')
        print(f'exists boolean value: {os.path.exists(out_dir)}')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        self.out_dir = out_dir
        self.logger = logging.getLogger(__name__)

    def __str__(self):
        return 'MemeEngine to create the meme with image and quote.'

    def make_meme(self, img_path, text, author, width=500) -> str:
        """
        Returns the generated image path of the created meme. The given image
        is proprocessed. This workflow is a little bit different
		depending on image type jpeg or png. The png image is transformed
		to a grayscale image, the jpg image is not transformed like this.

        input:
        img_path: (str) the path of the original image used for meme creation
        text: (str) the quote text body
        author: (str) the author of the quote text
		width: (int) new image width used for scaling

		return: the path of the created meme image
        """
        self.logger.info(f'make_meme call with PIL version: {PIL.__version__}')
        self.logger.info('First, we modify - preprocess - the given image.')
        mod_path = ImageIngestor.modify_image(img_path, width)

        # With this new preprocessed image object we create the meme;
        # text colour is white,
		# author info shall be written on a new line,
        # text position is randomly chosen
        meme_img = Image.open(mod_path)
        quote = text + '\n' + author
        self.logger.info(f'Second, we take care of the given quote: "{quote}"')
        font = ImageFont.truetype('arial.ttf', 15)    #'HelveticaNarrow-Bold', 20)
        txt_pos_x = random.choice(range(10, meme_img.size[0]-200))
        txt_pos_y = random.choice(range(10, meme_img.size[1]-30))
        draw = ImageDraw.Draw(meme_img)
        text_colour = 'white'
        # for position testing used: (10, 10) as starting point
        draw.multiline_text((txt_pos_x, txt_pos_y), quote, font=font, fill=text_colour)

        meme_img.show()
        img_name = pathlib.Path(mod_path).name
        meme_path = self.out_dir + '/' + img_name
        self.logger.info(f'MemeEngine: Path of created meme: {meme_path}')
        meme_img.save(meme_path)

        # remove the preprocessed, modified image
        try:
            self.logger.info(f'Remove preprocessed, modified image: {mod_path}')
            os.remove(mod_path)
        except OSError as err:
            self.logger.error(f'File could not be removed: {mod_path},\nerr: {err}')

        return str(meme_path)
