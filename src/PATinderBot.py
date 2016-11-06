'''
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
'''
import PACommon
import json
from os.path import os
import requests
from shutil import copyfile
import sys

from PACollageCreator import PACollageCreator
from PATinderUser import PATinderUser


class PATinderBot:
    def __init__(self):
        self._read_secrets_file()
        self._read_schools_file()
        self.headers = {
            'app_version': '3',
            'platform': 'ios'
        }
        self.collageCreator = PACollageCreator()

        self.user, self.tinder_token = self.tinder_login()
        self.analyze_photo_success_rate(self.user.get('photos', []))

    def run_tinder_bot(self):
        print('Tinder bot is running')

        for user in self._recommendations():

            if user is None:
                break

            action = self._like_or_nope(user)
            if action == 'like':
                match = self._like(user)
                if match:
                    status = 'match'
                else:
                    status = 'like'
            elif action == 'nope':
                status = 'nope'
                self._nope(user)

            if action != 'no_action':
                self._create_photo_cards(user, status)

        print('Tinder bot is finished')

    def _recommendations(self):
        h = self.headers
        h['X-Auth-Token'] = self.tinder_token
        r = requests.get('https://api.gotinder.com/user/recs', headers=h)
        if r.status_code == 401:
            raise Exception('HTTP Error 401 Unauthorized')
        elif r.status_code == 504:
            raise Exception('HTTP Error 504 Gateway timeout')

        if 'results' not in r.json():
            print(r.json())

        results = r.json().get('results')
        if results:
            for result in results:
                yield PATinderUser(result)

    def _like(self, user):
        print(' -> Like {} ({})'.format(user.name, user.id))
        try:
            u = 'https://api.gotinder.com/like/{}'.format(user.id)
            d = requests.get(u, headers=self.headers, timeout=0.7).json()
            return d.get('match')
        except KeyError:
            # Only raise key errors
            raise
        except:
            # Ignore all other errors
            pass

    def _nope(self, user):
        print(' -> Nope {} ({})'.format(user.name, user.id))
        try:
            u = 'https://api.gotinder.com/pass/{}'.format(user.id)
            requests.get(u, headers=self.headers, timeout=0.7).json()
        except KeyError:
            # Only raise key errors
            raise
        except:
            # Ignore all other errors
            pass

    def _like_or_nope(self, user):
        '''Determine the 'like action' for the given user: like, nope or no_action

        If there is at least one good school: like
        If not, if there is at least one unknown school: no_action
        If not: nope
        '''
        unknown_school = False
        for school in user.schools:
            school_id = school.get('id')
            if school_id in self.schools:
                if self.schools[school_id] == 1:
                    print('Approved school: {}'.format(school.get('name')))
                    return 'like'
            else:
                self._update_schools(school)
                unknown_school = True
        if unknown_school:
            return 'no_action'
        else:
            return 'nope'

    def _create_photo_cards(self, user, status):
        for photo in user.d['photos']:
            self.collageCreator.download_img(url=photo['url'])
        self.collageCreator.create_collage(user, status)

    def _read_secrets_file(self):
        secrets_file = self._get_secrets_file_name()
        with open(secrets_file) as f:
            self.secrets = json.loads(f.read())

    def _read_schools_file(self):
        self.schools = dict()
        schools_file = self._get_schools_file_name()
        if not os.path.isfile(schools_file):
            schools_template_file = 'schools_template.json'
            copyfile(schools_template_file, schools_file)

        self._clean_schools_file()
        with open(schools_file) as f:
            schools = json.loads(f.read())
            for school in schools:
                school_id = school.get('id')
                if school_id in self.schools:
                    print('School with id {} occurs multiple times in {}'.
                          format(school_id, schools_file))
                self.schools[school_id] = school.get('status')

    @staticmethod
    def _get_secrets_file_name():
        secrets_file = 'secrets.json'
        return os.path.join(PACommon.get_dir('json'), secrets_file)

    @staticmethod
    def _get_schools_file_name():
        schools_file = 'schools.json'
        return os.path.join(PACommon.get_dir('json'), schools_file)

    @staticmethod
    def get_facebook_auth_token_url():
        url = 'https://www.facebook.com/v2.6/dialog/oauth'
        params = {
            'api_key': '464891386855067',  # Tinder's App ID
            'redirect_uri': 'fbconnect://success',  # Tinder's whitelisted redirect URI
            'response_type': 'token',
            'scope': 'email,public_profile'
        }
        response = requests.get(url, params)
        return response.url

    def tinder_login(self) -> (dict, str):
        """
        Log in to Tinder using the Facebook oAuth token

        :return: (user's info dictionary, user's Tinder oAuth token)
        """
        h = self.headers
        h['content-type'] = 'application/json'
        url = 'https://api.gotinder.com/auth'
        params = {
            'facebook_id': self.secrets.get('FACEBOOK_ID'),
            'facebook_token': self.secrets.get('FACEBOOK_AUTH_TOKEN')
        }
        req = requests.post(
            url,
            headers=h,
            data=json.dumps(params)
        )

        if req.status_code == 401:
            print('401 Unauthorized: Could not get token with parameters {}'.format(params))
            sys.exit(0)

        result = req.json()
        user = result.get('user')
        tinder_token = result.get('token')
        return user, tinder_token

    @staticmethod
    def analyze_photo_success_rate(photos):
        """Analyze the photo success rates of the user"""
        print('*** Photo analysis ***\n')
        for photo in photos:
            url = photo.get('url')
            select_rate = photo.get('selectRate')
            success_rate = photo.get('successRate')
            print('{}: select rate = {}, success rate = {}'.format(url, select_rate, success_rate))
        print('\n')

    def _clean_schools_file(self):
        """Remove duplicate schools from the school list"""
        schools_file = self._get_schools_file_name()
        with open(schools_file) as f:
            schools = json.loads(f.read())

        unique_school_ids = []
        unique_schools = []
        for school in schools:
            school_id = school.get('id')
            if school_id not in unique_school_ids:
                unique_school_ids.append(school_id)
                unique_schools.append(school)

        unique_schools = sorted(unique_schools, key=lambda k: k['id'])
        unique_schools = sorted(unique_schools, key=lambda k: k['status'])

        with open(schools_file, 'w') as outfile:
            json.dump(unique_schools, outfile, indent=4)

    def _update_schools(self, school):
        schools_file = self._get_schools_file_name()
        print(' -> Adding school {} to {}'.format(school.get('name'), schools_file))
        with open(schools_file) as f:
            schools = json.loads(f.read())
        schools.append({'id': school.get('id'),
                        'name': school.get('name', None),
                        'status': 2})
        with open(schools_file, 'w') as outfile:
            json.dump(schools, outfile, indent=4)


if __name__ == '__main__':
    print('Visit this URL to retrieve your Facebook auth token:\n{}\n'.format(
        PATinderBot.get_facebook_auth_token_url()))

    tinder_bot = PATinderBot()
    for i in range(1):
        print('*** Run {} ***\n'.format(i + 1))
        tinder_bot.run_tinder_bot()
