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

from collage_creator import CollageCreator
from school_manager import ACTION_REQUIRED, APPROVED, SchoolManager
from secrets import TINDER_USER_ID, get_from_secrets
from tinder_service import TinderService
from tinder_user import TinderUser


class TinderBot:
    MAX_NUMBER_OF_PHOTOS = 6

    _collage_creator: CollageCreator = None

    def __init__(self):
        self.school_manager = SchoolManager()

        self.service = TinderService()
        self.user = self.service.get_user(get_from_secrets(TINDER_USER_ID))
        self.analyze_photo_success_rate(self.user.photos)

    def run(self):
        print('Tinder bot is running')

        for user in self.service.get_recommendations():
            if user is None:
                break

            action = self._like_or_nope(user)
            if action == 'like':
                match = self.service.like(user)
                if match:
                    status = 'match'
                else:
                    status = 'like'
                self._create_photo_cards(user, status)
                self._add_user_to_user_list(user, status)
            elif action == 'nope':
                self.service.nope(user)
                self._create_photo_cards(user, status='nope')
                self._add_user_to_user_list(user, status='nope')

        print('Tinder bot is finished\n')

    def _like_or_nope(self, user: TinderUser) -> str:
        """
        Determine the 'like action' for the given user: like, nope or no_action

        # TODO: Use an Enum for this
        If there is at least one good school: like
        If not, if there is at least one unknown school: no_action
        If not: nope

        # TODO: Check for bio
        """

        # Check for distance in km. If more than 100, it's an automatic reject
        if user.distance > 100:
            print(f'Distance is too large for {user}')
            return 'nope'

        # Check for schools the user went to. If she went to one of the approved schools,
        # it's an automatic like. If there is at least unknown school, no action is taken,
        # but the Bot user shall qualify the school in the schools file. If all schools are
        # rejected, the user is rejected.
        statuses = [self.school_manager.get_status(school) for school in user.schools]
        if APPROVED in statuses:
            print(f'Good school for {user}: {user.schools}')
            return 'like'
        elif ACTION_REQUIRED in statuses:
            print(f'Unknown school for {user}: {user.schools}')
            return 'no_action'
        else:
            # TODO: Fallthorugh for when there is no school
            print(f'No good school for {user}: {user.schools}')
            return 'nope'

    def _create_photo_cards(self, user: TinderUser, status: str):
        collage_creator = CollageCreator()
        for photo_index, photo in enumerate(user.d['photos']):
            if photo_index < self.MAX_NUMBER_OF_PHOTOS:
                collage_creator.download_img(url=photo['url'])
        collage_creator.create_collage(user, status)

    def _add_user_to_user_list(self, user: TinderUser, status: str):
        collage_creator = CollageCreator()
        collage_creator.append_to_user_list(user, status)

    @staticmethod
    def analyze_photo_success_rate(photos: [dict]):
        """
        Analyze the photo success rates of the user
        """

        print('*** Photo analysis ***\n')
        for photo in photos:
            url = photo.get('url')
            select_rate = photo.get('selectRate')
            success_rate = photo.get('successRate')
            print('{}: select rate = {}, success rate = {}'.format(url, select_rate, success_rate))
        print('\n')


if __name__ == '__main__':
    tinder_bot = TinderBot()
    tinder_bot.run()
