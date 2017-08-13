"""
PATinderBot: automatically like and capture Tinder recommendations
Copyright (C) 2016  physicalattraction

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math
import os
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image, ImageFont, ImageDraw

import common
from tinder_user import TinderUser


class CollageCreator(object):
    """
    Class that creates a collage based on a PATinderUser
    """

    def __init__(self):
        self.photos = list()
        self._img_size = 400
        self._margin = 20
        self._first_text = None

    def download_img(self, url: str):
        """

        :param url: string
        :return: Image
            Opened original image of the given article number.
            If output is None, this means that the requested image does not exist.
        """

        if url is None:
            return

        r = requests.get(url)
        try:
            img = Image.open(BytesIO(r.content))
            img = img.resize((self._img_size, self._img_size), Image.ANTIALIAS)
            self.photos.append(img)
        except OSError as e:
            # Print the error message, but continue downloading
            print(e)

    def create_collage(self, user: TinderUser, status: str):
        """
        Collect all photos and place user info under the photos
        """

        img = self._write_user_photos()
        try:
            img = self._write_user_info(img, user)
        except Exception as e:
            # Print the error message, but continue creating a collage
            print(e)
        img = self._add_bottom_margin(img)

        filename = '{}_{}.jpg'.format(user.name, user.id)
        full_img_name = os.path.join(self._get_img_dir(status), filename)
        img.save(full_img_name, quality=95, optimize=True)

    def append_to_user_list(self, user: TinderUser, status: str):
        """
        Append the user info to the correct user list
        """

        user_list_file = self._get_liked_user_list_file_name(status)
        with open(user_list_file, 'a+') as f:
            print('Append to file {}'.format(user_list_file))
            f.write(user.info_string)
            f.write('\n\n')

    def _write_user_photos(self):
        nr_photos = len(self.photos)
        if nr_photos == 1:
            width = self._img_size
        else:
            width = 2 * self._img_size
        height = int(math.ceil(nr_photos / 2.0) * self._img_size)
        img = Image.new(mode='RGB', size=(width, height), color='white')
        index_x = 0
        index_y = 0
        for photo in self.photos:
            x = index_x * self._img_size
            y = index_y * self._img_size
            img.paste(photo, box=(x, y, x + photo.size[0], y + photo.size[1]))
            if index_x == 0:
                # Move to the right
                index_x = 1
            elif index_x == 1:
                # Move below and back to the left
                index_x = 0
                index_y += 1
        return img

    def _write_user_info(self, img, user):
        self._first_text = True

        img = self._put_text_in_img(img, 'Naam: {}'.format(user.name))
        img = self._put_text_in_img(img, 'Leeftijd: {} jaar'.format(user.age))
        if len(user.jobs) > 0:
            img = self._put_text_in_img(img, 'Werk: {}'.format(', '.join(user.jobs)))
        if len(user.school_names) > 0:
            img = self._put_text_in_img(img, 'School: {}'.format(', '.join(user.school_names)))
        if len(user.common_friends) > 0:
            img = self._put_text_in_img(img, 'Vrienden: {}'.format(', '.join(user.common_friends)))

        img = self._put_text_in_img(img, 'Afstand: {} km'.format(user.distance))
        img = self._put_text_in_img(img, 'Bio: {}'.format(user.bio))

        return img

    def _put_text_in_img(self, img, text):
        """
        Put the relevant text of a person in the img.
        """

        assert (self._first_text is not None)

        font_size = 24
        line_height = font_size + 2
        if self._first_text:
            new_height = img.size[1] + line_height + self._margin
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
        x = self._margin
        if self._first_text:
            y = img.size[1] + self._margin
        else:
            y = img.size[1]

        # Draw the text
        if text:
            draw.text((x, y), text, fill='black', font=font)

        # Indicate that we have drawn at least one text
        self._first_text = False

        return result

    def _add_bottom_margin(self, img):
        result = Image.new(mode='RGB', size=(img.size[0], img.size[1] + self._margin), color='white')
        result.paste(img, (0, 0, img.size[0], img.size[1]))
        return result

    @staticmethod
    def _get_img_dir(status):
        """
        Return a string which contains the PATinderBot img directory for the given status
        """

        date_format = '%Y%m%d'
        today_dir = datetime.today().strftime(date_format)
        img_dir = os.path.join(common.get_dir('img'), status, today_dir)
        common.ensure_dir_exists(img_dir)
        return img_dir

    @staticmethod
    def _get_liked_user_list_file_name(status):
        """
        Return a string which contains the user list text file for the given status
        """

        liked_user_list_file = '{}d_users.txt'.format(status)
        return os.path.join(CollageCreator._get_img_dir(status), liked_user_list_file)


if __name__ == '__main__':
    pass
