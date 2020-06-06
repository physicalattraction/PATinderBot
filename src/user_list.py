import json
import os.path
from datetime import datetime
from typing import Any, Dict

import common
from enums import Status
from tinder_user import TinderUser

UserDict = Dict[str, Any]


class UserList:
    users: [UserDict]

    def __init__(self, status: Status):
        self.status = status
        self.users = self._read_users_from_file()

    def append(self, user: TinderUser):
        """
        Append the user info to the user list file
        """

        user = user.as_dict()
        user['time'] = datetime.now().strftime('%H:%M:%S')
        self.users.append(user)

    def _get_list_file_name(self) -> str:
        """
        Return a string which contains the full path to the user list json file for the given user list
        """

        json_dir = common.get_dir('json')

        date_format = '%Y%m%d'
        today = datetime.today().strftime(date_format)
        today_dir = os.path.join(json_dir, today)
        common.ensure_dir_exists(today_dir)

        list_file = f'{self.status.value}_users.json'
        return os.path.join(today_dir, list_file)

    def _read_users_from_file(self) -> [TinderUser]:
        path_to_file = self._get_list_file_name()
        if os.path.exists(path_to_file):
            with open(path_to_file, 'r') as f:
                return json.load(f)
        else:
            return []

    def _write_users_to_file(self, users: [TinderUser]):
        with open(self._get_list_file_name(), 'w') as f:
            return json.dump(users, f, indent=2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        If the user list goes out of memory, write the current user list to file
        """

        # TODO: This doesn't work yet, at least not in test case, not tested in production code
        self._write_users_to_file(self.users)
