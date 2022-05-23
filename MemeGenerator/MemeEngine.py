"""
Class to create and handle the meme images.

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
import textwrap
import traceback
import PIL
from PIL import Image, ImageDraw, ImageFont
from string import ascii_letters

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
        """Initialise the MemeEngine instance."""
        print(f'==> MemeEngine: __init__: out_dir: {out_dir}')
        print(f'exists boolean value: {os.path.exists(out_dir)}')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        self.font_path = './Fonts/'
        self.out_dir = out_dir
        self.logger = logging.getLogger(__name__)

    def __str__(self):
        """Return MemeEngine information."""
        return 'MemeEngine to create the meme with image and quote.'

    def make_meme(self, img_path, text, author, width=500) -> str:
        """
        Return the generated image path of the created meme.

        The given image is proprocessed. This workflow differs depending
        on image type jpeg or png. The png image is transformed to a
        grayscale image, the jpg image is not transformed like this.
        If the given text is too long, it is wrapped to fit on the image.

        Text wrapping with maximum of chars per line happens, converts
        width param from pixel size to character count dynamically. It
        depends on chosen font style (we use standard arial).
        Remember: image position starts top-left corner with coordinates
        (0,0).

        input:
        img_path: (str) the path of the original image used for meme creation
        text: (str) the quote text body
        author: (str) the author of the quote text
        width: (int) new image width used for scaling

        return: the path of the created meme image
        """
        self.logger.info(f'make_meme call with PIL version: {PIL.__version__}')
        self.logger.info('First, we modify - preprocess - the given image.')
        meme_path = "Note: no meme created, no valid image path given"

        try:
            mod_path = ImageIngestor.modify_image(img_path, width)

            # With this new preprocessed image object we create the meme;
            # text colour is white,
            # author info shall be written on a new line,
            # text position is randomly chosen
            meme_img = Image.open(mod_path)
            print(f'MEME IMAGE  width, height: {meme_img.size}')

            # text wrapping with dynamic text scaling according font chars
            # see: https://docs.python.org/3/library/textwrap.html
            font = ImageFont.truetype(self.font_path+'arial.ttf', 22)
            print("START TEXT WRAPPING with arial font ...")
            self.logger.info("START TEXT WRAPPING with arial font ...")

            # width scaling for horizontal adjustment
            avg_char_width = sum(font.getsize(char)[0] for char
                                 in ascii_letters) / len(ascii_letters)
            self.logger.info(f'-- avg_char_width: {avg_char_width}')
            # regarding image aesthetics of golden ratio (61.8%)
            max_char_count = int(meme_img.size[0] * .618 / avg_char_width)
            print(f'-- max_char_count: {max_char_count}')

            scaled_text = textwrap.fill(text=text, width=max_char_count)
            # scaled_text = get_scaled_txt(text = text,
            #                             font = font,
            #                             img_width = meme_img.size[0])
            print(f'==> calculated scaled_text: {scaled_text}')
            self.logger.info(f'==> calculated scaled_text: {scaled_text}')

            quote = scaled_text + '\n' + author
            print(f'generated quote is: {quote}')
            self.logger.info(f'We take care of the given quote: "{quote}"')

            # Add text to the image;
            # height scaling for vertical adjustment appears with image
            # and text size do an bottom upward shift if necessary
            draw = ImageDraw.Draw(meme_img)
            print(f'draw textsize w, h: {draw.textsize(quote, font=font)}')
            self.logger.info(f'textsize: {draw.textsize(quote, font=font)}"')
            txt_pos_x = random.choice(range(10, meme_img.size[0]-280))
            txt_pos_y = random.choice(
                range(10,
                      meme_img.size[1]-draw.textsize(quote, font=font)[1]-10))

            # colour setting for fill param
            text_colour = 'white'      # 'rgb(255, 255, 255)'
            # see: https://colorcodes.io/green/dark-green-color-codes/
            # text_colour = 'rgb(00, 255, 00)'  # neon green (default green)
            # text_colour = '#3A6152'   # other kind of green, not visible
            # see: https://colorcodes.io/beige-color-codes/
            # text_colour = 'rgb(227, 212, 173)'  # Desert Sand
            # text_colour = 'rgb(211, 188, 141)'    # Khaki
            draw.text(xy=(txt_pos_x, txt_pos_y),
                      text=quote, font=font,
                      fill=text_colour)

            meme_img.show()

            # create meme_path
            img_name = pathlib.Path(mod_path).name
            meme_path = self.out_dir + '/' + img_name
            self.logger.info(f'MemeEngine: Path of created meme: {meme_path}')
            meme_img.save(meme_path)

            # remove the preprocessed, modified image
            self.logger.info(f'Remove preprocessed image: {mod_path}')
            os.remove(mod_path)
        except IOError as io_err:
            msg = f'Image {mod_path} cannot be opened: err: {io_err}'
            self.logger.error(msg)
            traceback.print_tb(io_err.__traceback__)
        except NameError as name_err:
            f'make_meme got wrong Name args: err: {name_err}'
            self.logger.error(msg)
            traceback.print_tb(name_err.__traceback__)
        except AttributeError as attr_err:
            msg = f'make_meme got wrong Attribute args: err: {attr_err}'
            self.logger.error(msg)
            traceback.print_tb(attr_err.__traceback__)
        except FileNotFound as filenotfound_err:
            msg = f'Imagefile not found: {img_path},\nerr: {filenotfound_err}'
            self.logger.error(msg)
            traceback.print_tb(filenotfound_err.__traceback__)
        except OSError as os_err:
            msg = f'File not be removed: {mod_path},\nerr: {os_err}'
            self.logger.error(msg)
            traceback.print_tb(os_err.__traceback__)

        return str(meme_path)
