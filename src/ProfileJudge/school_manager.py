import json
import os.path
import string
from typing import Set

import common
from type_hinting import SchoolDict

SCHOOLS_APPROVE_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_approve_words.json')
SCHOOLS_REJECT_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_reject_words.json')
SCHOOLS_REVIEW_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_review_words.json')

# TODO: Turn into an Enum
REJECTED = 0
APPROVED = 1
ACTION_REQUIRED = 2


class WordListMixin:
    _approve_words: Set[str] = None
    _reject_words: Set[str] = None
    _review_words: Set[str] = None

    @property
    def approve_words(self):
        if not self._approve_words:
            self._approve_words = self._read_file(SCHOOLS_APPROVE_WORDS_FILE)
        return self._approve_words

    @property
    def reject_words(self):
        if not self._reject_words:
            self._reject_words = self._read_file(SCHOOLS_REJECT_WORDS_FILE)
        return self._reject_words

    @property
    def review_words(self):
        if not self._review_words:
            self._review_words = self._read_file(SCHOOLS_REVIEW_WORDS_FILE)
        return self._review_words

    def add_word_for_review(self, value: str):
        if value not in self.review_words:
            self._review_words.add(value)
            with open(SCHOOLS_REVIEW_WORDS_FILE, 'w') as f:
                json.dump(sorted(self._review_words), f, indent=2)

    def _read_file(self, filepath: str) -> Set[str]:
        self._ensure_exists(filepath)
        with open(filepath, 'r') as f:
            result = set(json.load(f))
        with open(filepath, 'w') as f:
            # Perform maintenance on the file by sorting the contents alphabetically
            json.dump(sorted(result), f, indent=2)
        return result

    def _ensure_exists(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            # If there is a school file missing, generate it empty
            with open(filepath, 'w') as f:
                json.dump([], f)


class SchoolManager(WordListMixin):
    def __init__(self, verbosity: int = 0):
        self.verbosity = verbosity

    def get_status(self, school: SchoolDict) -> int:
        """
        Return the status for the given school
        """

        try:
            # Clean up the name: make all letters lower case and remove all non alphanumerical characters
            name = school['name']
            clean_name = name.lower()
            clean_name = ''.join(letter for letter in clean_name
                                 if letter in string.ascii_lowercase + string.digits + ' ')
        except KeyError:
            # Somehow, some schools don't have a name. Since we qualify all schools based on
            # their name, these schools are useless, and hence we automatically reject them.
            if self.verbosity >= 1:
                print(f'School has no name: {school}')
            return REJECTED

        words = clean_name.split(' ')
        if any(word in self.approve_words for word in words):
            # When any word is approved, we know it's a good school
            if self.verbosity >= 1:
                print(f'At least one words in school name is approved: {name}')
            return APPROVED
        elif all(word in self.reject_words for word in words):
            # When all words are rejected, we know it's a bad school
            if self.verbosity >= 1:
                print(f'All words in school name are rejected: {name}')
            return REJECTED
        else:
            # In all other cases, we need to review the words and take no action
            if self.verbosity >= 1:
                print(f'All words in school name are for review: {clean_name}')
            for word in words:
                if word not in self.reject_words:
                    self.add_word_for_review(word)
            return ACTION_REQUIRED


if __name__ == '__main__':
    print(SchoolManager(verbosity=1).get_status({'name': 'PABO Amsterdam'}))
