import json
import os.path
import string
from abc import ABC
from typing import Set

import common
from ProfileJudge.vote import Vote
from logger import Logger


class WordListMixin:
    # This field name needs to be set by the concrete implementations
    FIELD_NAME: str = None

    _approve_words: Set[str] = None
    _reject_words: Set[str] = None
    _review_words: Set[str] = None

    @property
    def approve_words_file(self) -> str:
        return os.path.join(common.get_dir('json'), f'{self.FIELD_NAME}_approve_words.json')

    @property
    def reject_words_file(self) -> str:
        return os.path.join(common.get_dir('json'), f'{self.FIELD_NAME}_reject_words.json')

    @property
    def review_words_file(self) -> str:
        return os.path.join(common.get_dir('json'), f'{self.FIELD_NAME}_review_words.json')

    @property
    def approve_words(self):
        if self._approve_words is None:
            self._approve_words = self._read_file(self.approve_words_file)
        return self._approve_words

    @property
    def reject_words(self):
        if self._reject_words is None:
            self._reject_words = self._read_file(self.reject_words_file)
        return self._reject_words

    @property
    def review_words(self):
        if self._review_words is None:
            self._review_words = self._read_file(self.review_words_file)
        return self._review_words

    def add_word_for_review(self, value: str):
        if value not in self.review_words:
            self._review_words.add(value)
            with open(self.review_words_file, 'w') as f:
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


class WordJudge(WordListMixin, ABC):
    """
    Abstract base class that judges a specific field of the user's profiel based on individual words in it
    """

    def judge_by_words(self, name: str) -> Vote:
        assert self.FIELD_NAME is not None

        clean_name = name.lower()
        clean_name = ''.join(letter for letter in clean_name
                             if letter in string.ascii_lowercase + string.digits + ' ')
        words = clean_name.split(' ')
        if any(word in self.approve_words for word in words):
            # When any word is approved, we know it's a good school
            Logger.log(f'At least one word in {self.FIELD_NAME} is approved: {name}', level=3)
            return Vote.approve
        elif all(word in self.reject_words for word in words):
            # When all words are rejected, we know it's a bad school
            Logger.log(f'All words in {self.FIELD_NAME} are rejected: {name}', level=3)
            return Vote.reject
        else:
            # In all other cases, we need to review the words and take no action
            Logger.log(f'All words in {self.FIELD_NAME} are for review: {clean_name}', level=3)
            for word in words:
                if word not in self.reject_words:
                    self.add_word_for_review(word)
            return Vote.review
