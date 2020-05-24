import json
import os.path
from operator import itemgetter
from shutil import copyfile
from typing import Dict, List, Union

import common

SCHOOLS_FILE = os.path.join(common.get_dir('json'), 'schools.json')
SCHOOLS_TEMPLATE_FILE = os.path.join(common.get_dir('json'), 'schools_template.json')

APPROVE_WORDS = ['universiteit', 'hogeschool', 'university']

# TODO: Turn into an Enum
REJECTED = 0
APPROVED = 1
ACTION_REQUIRED = 2

SchoolDict = Dict[str, Union[str, int]]


class SchoolManager:
    _school_statuses: Dict[str, int] = {}  # Look up from school id to status

    @property
    def school_statuses(self):
        if not self._school_statuses:
            self._clean_schools_file()
            self._school_statuses = {school['id']: school['status'] for school in self._read_schools_file()}
        return self._school_statuses

    def get_status(self, school: SchoolDict) -> int:
        """
        Return the status for the given school
        """

        if not school.get('name'):
            # Somehow, some schools don't have a name. Since we qualify all schools based on
            # their name, these schools are useless, and hence we automatically reject them.
            return REJECTED
        name = school['name']

        if not school.get('id'):
            # Somehow, some schools don't have an ID. If they don't have an ID, we don't store
            # them in the file. We do judge them on the spot, based on the name.
            if any(word in name.lower() for word in APPROVE_WORDS):
                return APPROVED
            else:
                return REJECTED
        school_id = school['id']

        if school_id in self.school_statuses:
            return self.school_statuses[school_id]
        else:
            return self._add_school(school)

    def _add_school(self, school: SchoolDict) -> int:
        """
        Add the given school to the school file
        """

        assert school.get('id'), f'School must have an id: {school}'
        assert school.get('name'), f'School must have a name: {school}'

        school_id, name = school['id'], school['name']
        print(f' -> Adding school {name} to {SCHOOLS_FILE}')
        schools = self._read_schools_file()

        if any(word in name.lower() for word in APPROVE_WORDS):
            status = APPROVED
        else:
            status = ACTION_REQUIRED
        schools.append({'id': school_id, 'name': name, 'status': status})
        self._write_schools_file(schools)
        return status

    def _read_schools_file(self) -> List[SchoolDict]:
        """
        Read the list of schools from the schools file
        """

        if not os.path.isfile(SCHOOLS_FILE):
            copyfile(SCHOOLS_TEMPLATE_FILE, SCHOOLS_FILE)

        with open(SCHOOLS_FILE) as fp:
            return json.load(fp)

    def _write_schools_file(self, schools: List[SchoolDict]):
        """
        Write the input list of schools to the schools file
        """

        with open(SCHOOLS_FILE, 'w') as fp:
            json.dump(schools, fp, indent=4)

    def _clean_schools_file(self):
        """
        Remove duplicate schools from the school list
        """

        schools = self._read_schools_file()
        id_to_school = {school['id']: school for school in schools}
        unique_schools = sorted(id_to_school.values(), key=itemgetter('status', 'id'))
        self._write_schools_file(unique_schools)
