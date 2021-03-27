from ProfileJudge.enums import Vote
from ProfileJudge.vote_logger_mixin import VoteLoggerMixin
from logger import Logger
from tinder_user import TinderUser


class DistanceJudge(VoteLoggerMixin):
    def vote(self, user: TinderUser) -> Vote:
        # Check for distance in km
        info = f'Distance = {user.distance} km'
        if user.distance < 20:
            # If less than 20 km, I want to check them out manually
            return self._vote(info, Vote.review, 'Inside Amsterdam')
        elif user.distance > 200:
            # If outside The Netherlands, automatic reject
            return self._vote(info, Vote.reject, 'Outside The Netherlands')
        else:
            return self._vote(info, Vote.approve, 'Inside The Netherlands, but outside Amsterdam')


if __name__ == '__main__':
    Logger.max_level = 2
    DistanceJudge().vote(TinderUser({
        'name': 'Tessa', 'distance_mi': 120, 'birth_date': '1986-04-03T00:00:00.000Z',
        'schools': [{'name': 'PABO Amsterdam'}, {'name': 'MBO Amsterdam'}]
    }))
