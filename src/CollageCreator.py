'''
Created on Mar 19, 2015

@author: Erwin Rossen
'''

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import os
import requests
import math


class CollageCreator(object):
    '''
    Class that creates a collage based on a TinderUser
    '''

    def __init__(self):
        self.photos = list()
        self.__img_size = 400
        self.__margin = 20
        self.__first_text = None

    def download_img(self, url):
        '''Download an image as a PIL object

        If the img is not present yet, it is downloaded from the specified URL.

        Inputs:
        -------
        url: string

        Outputs:
        --------
        img: Image
            Opened original image of the given article number.
            If img = None, this means that the requested image does not exist.
        '''

        if url is None:
            return
        r = requests.get(url)
        try:
            img = Image.open(BytesIO(r.content))
            img = img.resize((self.__img_size, self.__img_size), Image.ANTIALIAS)
            self.photos.append(img)
        except OSError as e:
            # Print the error message, but continue downloading
            print(e)

    def create_collage(self, user, status):
        '''
        Collect all photos and place user info under the photos
        '''

        nr_photos = len(self.photos)
        if nr_photos == 1:
            W = self.__img_size
        else:
            W = 2 * self.__img_size
        H = int(math.ceil(nr_photos / 2.0) * self.__img_size)

        img = Image.new(mode='RGB', size=(W, H), color='white')

        index_x = 0
        index_y = 0
        for photo in self.photos:
            x = index_x * self.__img_size
            y = index_y * self.__img_size
            img.paste(photo, box=(x, y, x + photo.size[0], y + photo.size[1]))
            if index_x == 0:
                # Move to the right
                index_x = 1
            elif index_x == 1:
                # Move below and back to the left
                index_x = 0
                index_y += 1
        img = self.__write_user_info(img, user)
        img = self.__add_bottom_margin(img)

        filename = '{}_{}.jpg'.format(user.name, user.id)
        full_img_name = os.path.join(self.__get_img_dir(status), filename)
        img.save(full_img_name, quality=95, optimize=True)

    def __write_user_info(self, img, user):
        self.__first_text = True

        img = self.__put_text_in_img(img, 'Naam: {}'.format(user.name))
        img = self.__put_text_in_img(img, 'Leeftijd: {} jaar'.format(user.age))
        if len(user.jobs) > 0:
            img = self.__put_text_in_img(img, 'Werk: {}'.
                                         format(', '.join(user.jobs)))
        if len(user.school_names) > 0:
            img = self.__put_text_in_img(img, 'School: {}'.
                                         format(', '.join(user.school_names)))
        if len(user.common_friends) > 0:
            img = self.__put_text_in_img(img, 'Vrienden: {}'.
                                         format(', '.join(user.common_friends)))

        img = self.__put_text_in_img(img, 'Afstand: {} km'.format(user.distance))
        img = self.__put_text_in_img(img, 'Bio: {}'.format(user.bio))

        return img

    def __put_text_in_img(self, img, text):
        '''
        Put the relevant text of a person in the img.
        '''

        assert(self.__first_text is not None)

        font_size = 24
        line_height = font_size + 2
        if (self.__first_text):
            new_height = img.size[1] + line_height + self.__margin
        else:
            new_height = img.size[1] + line_height

        # Create more space to output text
        result = Image.new(mode='RGB', size=(img.size[0], new_height), color='white')
        result.paste(img, (0, 0, img.size[0], img.size[1]))

        # Initialize draw object
        draw = ImageDraw.Draw(result)

        # Define font
        font = ImageFont.truetype("Trebuchet MS Bold.ttf", font_size)

        # Define text location
        x = self.__margin
        if self.__first_text:
            y = img.size[1] + self.__margin
        else:
            y = img.size[1]

        # Draw the text
        draw.text((x, y), text, fill='black', font=font)

        # Indicate that we have drawn at least one text
        self.__first_text = False

        return result

    def __add_bottom_margin(self, img):
        result = Image.new(mode='RGB',
                           size=(img.size[0], img.size[1] + self.__margin),
                           color='white')
        result.paste(img, (0, 0, img.size[0], img.size[1]))
        return result

    def __ensure_dir_exists(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

    def __get_img_root_dir(self):
        '''Return a string which contains the root ERTinderBot img directory.

        Current directory structure:
        ERTinderBot
            src
                CollageCreator
            img
                like
                match
                nope
        '''
        current_dir = os.path.dirname(__file__)
        img_root_dir = os.path.join(current_dir, '..', 'img')
        self.__ensure_dir_exists(img_root_dir)
        return img_root_dir

    def __get_img_dir(self, status):
        '''Return a string which contains the ERTinderBot img directory for the given status.'''
        img_dir = os.path.join(self.__get_img_root_dir(), status)
        self.__ensure_dir_exists(img_dir)
        return img_dir

if __name__ == '__main__':
    pass
