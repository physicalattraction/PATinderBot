from ProfileJudge.vote import Vote
from ProfileJudge.vote_logger_mixin import VoteLoggerMixin
from logger import Logger
from tinder_user import TinderUser


class BioJudge(VoteLoggerMixin):
    def vote(self, user: TinderUser) -> Vote:
        """
        Check for the presence of a bio

        Presence is defined as:
        - There is something written
        - They're not all emoji's
        - There are at least 4 words
        """

        bio = user.bio
        if self._bio_is_present(bio):
            return self._vote(f'Bio: {bio}', Vote.approve, 'Bio is present')
        else:
            return self._vote(f'Bio: {bio}', Vote.reject, 'Bio is absent')

    def _bio_is_present(self, bio: str) -> bool:
        bio = bio.encode('ascii', 'ignore').decode()  # Remove all non-ASCII characters, like emojis
        return len(bio.split(' ')) >= 4  # Check for at least four different words in the bio


if __name__ == '__main__':
    Logger.max_level = 2
    BioJudge().vote(TinderUser({
        'name': 'Tessa', 'distance_mi': 120, 'birth_date': '1986-04-03T00:00:00.000Z',
        'schools': [{'name': 'PABO Amsterdam'}, {'name': 'MBO Amsterdam'}],
        'bio': '😊'
    }))
