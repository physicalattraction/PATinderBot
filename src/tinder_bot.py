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

import random
import time

from ProfileJudge.profile_judge import ProfileJudge
from collage_creator import CollageCreator
from enums import Status, SwipeAction
from logger import Logger
from secrets import TINDER_USER_ID, get_from_secrets
from tinder_service import TinderService
from tinder_user import TinderUser


class TinderBot:
    MAX_NUMBER_OF_PHOTOS = 6

    def __init__(self):
        self.profile_judge = ProfileJudge()
        self.service = TinderService()
        self.user = self.service.get_user(get_from_secrets(TINDER_USER_ID))
        Logger.log(f'TinderBot initialized for {self.user.name}. Liked today: {CollageCreator().nr_liked_today}.')

    def run(self, nr_profiles: int = 10):
        Logger.log('TinderBot is running')

        nr_profiles_checked = 0
        while True:
            # The function get_recommendations returns ±10 profiles, determined by Tinder
            # We therefore need to call this function multiple times if we want to run
            # the bot on more profiles.
            for user in self.service.get_recommendations():
                if user is None:
                    break

                nr_profiles_checked += 1
                Logger.log(f'{nr_profiles_checked}/{nr_profiles}', level=1)

                self._like_or_nope(user)

                if nr_profiles_checked >= nr_profiles:
                    Logger.log(f'TinderBot is finished. Liked today: {CollageCreator().nr_liked_today}.')
                    return

    def analyze_photo_success_rate(self):
        """
        Analyze the photo success rates of the user
        """

        Logger.log('*** Photo analysis ***')
        for photo in self.user.photos:
            url = photo.get('url')
            select_rate = photo.get('selectRate')
            success_rate = photo.get('successRate')
            Logger.log(f'{url}: select rate = {select_rate}, success rate = {success_rate}', level=1)

    def _like_or_nope(self, user: TinderUser) -> None:
        action = self.profile_judge.like_or_nope(user)
        if action == SwipeAction.like:
            match = self.service.like(user)
            if match:
                Logger.log("*** It's a match!! ***\n", level=1)
                status = Status.matched
            else:
                status = Status.liked
            self._create_photo_cards(user, status)
        elif action == SwipeAction.nope:
            self.service.nope(user)
            # In order to not look like a bot, we wait a random time around 1 second
            # For like this is not necessary, since we create a photo collage for them,
            # which takes a similar amount of time
            time.sleep(random.uniform(0.7, 1.2))
        elif action == SwipeAction.no_action:
            # Explicitly do nothing
            pass

    def _create_photo_cards(self, user: TinderUser, status: Status):
        collage_creator = CollageCreator()
        for photo_index, photo in enumerate(user.d['photos']):
            if photo_index < self.MAX_NUMBER_OF_PHOTOS:
                collage_creator.download_img(url=photo['url'])
        collage_creator.create_collage(user, status)


if __name__ == '__main__':
    Logger.max_level = 1
    tinder_bot = TinderBot()
    # tinder_bot.analyze_photo_success_rate()
    tinder_bot.run(nr_profiles=1000)
