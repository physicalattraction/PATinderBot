import os.path

import common
from ProfileJudge.word_manager import REJECTED, WordManager
from type_hinting import SchoolDict


class SchoolManager(WordManager):
    APPROVE_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_approve_words.json')
    REJECT_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_reject_words.json')
    REVIEW_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_review_words.json')

    def get_status(self, school: SchoolDict) -> int:
        """
        Return the status for the given school
        """

        try:
            # Clean up the name: make all letters lower case and remove all non alphanumerical characters
            name = school['name']
        except KeyError:
            # Somehow, some schools don't have a name. Since we qualify all schools based on
            # their name, these schools are useless, and hence we automatically reject them.
            if self.verbosity >= 1:
                print(f'School has no name: {school}')
            return REJECTED

        return self.judge_by_words(name)


if __name__ == '__main__':
    print(SchoolManager(verbosity=1).get_status({'name': 'PABO Amsterdam'}))
