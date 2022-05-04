from ProfileJudge.vote import Vote
from ProfileJudge.vote_logger_mixin import VoteLoggerMixin
from ProfileJudge.word_judge import WordJudge
from logger import Logger
from tinder_user import TinderUser


class NameJudge(VoteLoggerMixin, WordJudge):
    """
    Judge a user based on their name

    Use case: In some cases, Tinder is "teasing" the user by showing the name of a user that has already liked them.
              In those cases, like the user instantly, for an instant match.
    """

    FIELD_NAME = 'name'

    def vote(self, user: TinderUser) -> Vote:
        vote = self.judge_by_words(user.name)
        return self._vote('Judged by name', vote, 'Judged by name')


if __name__ == '__main__':
    Logger.max_level = 2
    print(NameJudge().approve_words_file)
    NameJudge().vote(TinderUser({
        'name': 'Julia', 'distance_mi': 120, 'birth_date': '1986-04-03T00:00:00.000Z',
        'schools': [{'name': 'PABO Amsterdam'}, {'name': 'MBO Amsterdam'}]
    }))
