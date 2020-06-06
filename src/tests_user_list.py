import filecmp
import os.path
import shutil
from unittest import TestCase
from unittest.mock import patch

import common
from enums import Status
from tinder_user import TinderUser
from user_list import UserList

T1 = '18:49:34'


class UserListTestCase(TestCase):
    test_data_dir = common.get_dir('test_data')
    tmp_dir = common.get_dir('tmp')
    user_list_file = os.path.join(test_data_dir, 'liked_users.json')
    tmp_user_list_file = os.path.join(tmp_dir, 'liked_users.json')

    def setUp(self):
        # TODO: Make this mock data vailable when writing test cases for TinderUser class
        self.tinder_user = TinderUser({
            '_id': '5699',
            'bio': 'This is my bio',
            'birth_date': '1981-06-09T16:22:21.851Z',
            'name': 'John',
            'photos': [{'id': '3d32', 'type': 'image',
                        'created_at': '2019-09-19T08:56:34.119Z', 'updated_at': '2020-05-15T20:42:48.595Z',
                        'url': 'https://images-ssl.gotinder.com/5699/3d32.jpg',
                        'fileName': '3d32.jpg', 'extension': 'jpg',
                        'xoffset_percent': 0, 'yoffset_percent': 0, 'xdistance_percent': 1, 'ydistance_percent': 1}],
            'jobs': [{'company': {'name': 'My company'}, 'title': {'name': 'CTO'}}],
            'schools': [{'name': 'My University', 'id': '1081'}],
            'gender': 0,
            'city': {'name': 'Amsterdam', 'region': 'Netherlands'},
            'distance_mi': 10}
        )

        if os.path.exists(self.tmp_user_list_file):
            os.remove(self.tmp_user_list_file)

    def tearDown(self):
        if os.path.exists(self.tmp_user_list_file):
            os.remove(self.tmp_user_list_file)

    def test_that_users_are_initialized_as_empty_list_without_file(self):
        path_to_file = self.user_list_file + 'does_not_exist'
        self.assertFalse(os.path.exists(path_to_file))
        with patch.object(UserList, '_get_list_file_name', return_value=path_to_file):
            user_list = UserList(Status.liked)
            self.assertListEqual([], user_list.users)

    def test_that_users_are_initialized_with_file(self):
        with patch.object(UserList, '_get_list_file_name', return_value=self.user_list_file):
            user_list = UserList(Status.liked)
        self.assertEqual(1, len(user_list.users))
        user = user_list.users[0]
        self.assertEqual(self.tinder_user.id, user['id'])
        self.assertEqual(T1, user['time'])

    def test_that_users_can_be_appended(self):
        with patch.object(UserList, '_get_list_file_name', return_value=self.tmp_user_list_file):
            user_list = UserList(Status.liked)
            # TODO: Preferably I would mock datetime.now() here and check that it's set
            user_list.append(self.tinder_user)
        self.assertEqual(1, len(user_list.users))
        user = user_list.users[0]
        self.assertEqual(self.tinder_user.id, user['id'])

    def test_that_user_list_can_be_written_to_file(self):
        with patch.object(UserList, '_get_list_file_name', return_value=self.tmp_user_list_file):
            user_list = UserList(Status.liked)
            user_list.append(self.tinder_user)
            user_list.users[0]['time'] = T1
            user_list._write_users_to_file(user_list.users)
            self._compare_file_with_file(self.tmp_user_list_file, self.user_list_file)

    def _compare_file_with_file(self, input_filepath: str, reference_filepath: str, name: str = 'file',
                                write_first: bool = False) -> None:
        """
        Compare the input file with a reference file

        :param input_filepath: Full path to the input file to check
        :param reference_filepath: Full path to the reference file to check with
        :param name: Name of the file to check, used in logging
        :param write_first: Flag to indicate whether we first need to write the reference file
        """

        # TODO: Create a FileComparingMixin

        if write_first:
            shutil.copyfile(input_filepath, dst=reference_filepath)

        if not filecmp.cmp(input_filepath, reference_filepath):
            reference_dir, reference_filename = os.path.split(reference_filepath)
            generated_filename = f'generated_{reference_filename}'
            generated_filepath = os.path.join(reference_dir, generated_filename)
            shutil.copyfile(src=input_filepath, dst=generated_filepath)
            msg = f'Generated {name} written to: {generated_filename}'
            self.fail(msg)
