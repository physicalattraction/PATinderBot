import os.path

import common
from ProfileJudge.enums import Vote
from ProfileJudge.vote_logger_mixin import VoteLoggerMixin
from ProfileJudge.word_judge import WordJudge
from logger import Logger
from tinder_user import TinderUser
from type_hinting import SchoolDict


class SchoolJudge(VoteLoggerMixin, WordJudge):
    APPROVE_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_approve_words.json')
    REJECT_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_reject_words.json')
    REVIEW_WORDS_FILE = os.path.join(common.get_dir('json'), 'school_review_words.json')

    FIELD_NAME = 'school'

    def vote(self, user: TinderUser) -> Vote:
        """
        Check for schools the user went to

        If she went to one of the approved schools: like
        If there is at least one unknown school: review
        If all schools are rejected: reject
        If there are no schools: no info
        """

        votes = [self._get_vote_for_school(school) for school in user.schools]
        schools_str = 'Schools = ' + ', '.join(school['name'] for school in user.schools)
        if Vote.approve in votes:
            return self._vote(schools_str, Vote.approve, 'At least one approved')
        elif Vote.review in votes:
            return self._vote(schools_str, Vote.review, 'At least one unknown')
        elif not votes:
            return self._vote(schools_str, Vote.no_info, 'Empty list')
        else:
            return self._vote(schools_str, Vote.reject, 'All rejected')

    def _get_vote_for_school(self, school: SchoolDict) -> Vote:
        """
        Return the status for the given school
        """

        try:
            # Clean up the name: make all letters lower case and remove all non alphanumerical characters
            name = school['name']
        except KeyError:
            # Somehow, some schools don't have a name. Since we qualify all schools based on
            # their name, these schools are useless, and hence we automatically reject them.
            Logger.log(f'School has no name: {school}', level=2)
            return Vote.reject

        return self.judge_by_words(name)


if __name__ == '__main__':
    Logger.max_level = 2
    SchoolJudge().vote(TinderUser({
        'name': 'Tessa', 'distance_mi': 120, 'birth_date': '1986-04-03T00:00:00.000Z',
        'schools': [{'name': 'PABO Amsterdam'}, {'name': 'MBO Amsterdam'}]
    }))
