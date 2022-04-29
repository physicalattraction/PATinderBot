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
from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict

from type_hinting import TinderUserDict


class TinderUser:
    """
    Representation of a Tinder User
    """

    def __init__(self, data_dict: TinderUserDict):
        self.d = data_dict

    @property
    def id(self) -> str:
        return self.d['_id']

    @property
    def bio(self) -> str:
        """
        Return a representation of the user's bio
        """

        bio = self.d.get('bio')
        if bio:
            bio = bio.replace('\n', '. ')
        return bio

    @property
    def name(self) -> str:
        """
        Return the user name
        """

        return self.d.get('name')

    @property
    def age(self) -> int:
        """
        Return the user age in years

        Note: many users have the following setting:
            "birth_date_info": "fuzzy birthdate active, not displaying real birth_date"
        In practice, this means that the birthday is not precise, they are all on the same day.
        """

        raw = self.d.get('birth_date')
        if raw:
            birth_date = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            now = datetime.now()
            age = now - birth_date
            return age.days // 365

        return 0

    @property
    def jobs(self) -> [str]:
        """
        Return a list of jobs. Format per element: "title - company"
        """

        jobs = list()
        if 'jobs' in self.d:
            for job in self.d.get('jobs'):
                this_job = list()
                if 'title' in job and 'name' in job['title']:
                    this_job.append(job['title']['name'])
                if 'company' in job and 'name' in job['company']:
                    this_job.append(job['company']['name'])
                if len(this_job) > 0:
                    this_job_string = ' - '.join(this_job)
                    jobs.append(this_job_string)
        return jobs

    @property
    def schools(self) -> [dict]:
        """
        Return a list of schools. Each school is a dictionary with id and name
        """

        if 'schools' in self.d:
            return self.d.get('schools')
        else:
            return list()

    @property
    def school_names(self) -> [str]:
        """
        Return a list of school names
        """

        return [school.get('name') for school in self.schools if school.get('name')]

    @property
    def common_friends(self) -> [str]:
        """
        Return a list of common friends. Format per element: "name"
        """

        common_friends = list()
        for friend in common_friends:
            print(friend)
            common_friends.append(friend['name'])
        return common_friends

    @property
    def distance(self) -> int:
        """
        Return the distance in km. Format: integer
        """

        try:
            return int(round(self.d['distance_mi'] * 1.609))
        except (KeyError, TypeError):
            return 0

    @property
    def info_string(self) -> str:
        """
        Return a multiline info string about the user
        """

        txt_elements = OrderedDict()
        txt_elements['Id'] = self.id
        txt_elements['Naam'] = self.name
        txt_elements['Leeftijd'] = f'{self.age} jaar'
        if len(self.jobs) > 0:
            txt_elements['Werk'] = ', '.join(self.jobs)
        if len(self.school_names) > 0:
            txt_elements['School'] = ', '.join(self.school_names)
        if len(self.common_friends) > 0:
            txt_elements['Vrienden'] = ', '.join(self.common_friends)
        txt_elements['Afstand'] = f'{self.distance} km'
        txt_elements['Bio'] = self.bio

        txt_lines = [f'{key}: {value}' for key, value in txt_elements.items()]
        return '\n'.join(txt_lines)

    @property
    def photos(self):
        return self.d['photos']

    def as_dict(self):
        """
        Return a dictionary representation of the current object, removing keys with empty values
        """

        result = {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'distance': self.distance,
            'bio': self.bio,
            'jobs': ', '.join(self.jobs),
            'school_names': ', '.join(self.school_names),
            'common_friends': ', '.join(self.common_friends),
            'photos': [photo['url'] for photo in self.photos],
        }
        return {k: v for k, v in result.items() if v}

    def __unicode__(self) -> str:
        return f'{self.name} ({self.age}), {self.distance} km'

    def __str__(self) -> str:
        return f'{self.name} ({self.age}), {self.distance} km, {self.bio}'

    def __repr__(self) -> str:
        return f'{self.name} ({self.age}), {self.distance} km'
