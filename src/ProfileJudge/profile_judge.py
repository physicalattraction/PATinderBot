from ProfileJudge.distance_judge import DistanceJudge
from ProfileJudge.enums import Vote
from ProfileJudge.school_judge import SchoolJudge
from enums import SwipeAction
from logger import Logger
from tinder_user import TinderUser


class ProfileJudge:
    """
    Class responsible for determining the swipe action for a given user
    """

    def __init__(self):
        self.distance_judge = DistanceJudge()
        self.school_judge = SchoolJudge()

    def like_or_nope(self, user: TinderUser) -> SwipeAction:
        """
        Determine the SwipeAction for the given user, based on votes from different judges

        # TODO: Check for work and/or bio
        """

        Logger.log(f'Judging {user}', level=1)

        # First check for distance, this can determine the action regardless of the other votex
        distance_vote = self.distance_judge.vote(user)
        if distance_vote == Vote.reject:
            return self._action(SwipeAction.nope, 'Too far away.')
        elif distance_vote == Vote.review:
            return self._action(SwipeAction.no_action, 'Too close to automate.')

        # Then check for schools
        school_vote = self.school_judge.vote(user)
        if school_vote == Vote.approve:
            return self._action(SwipeAction.like, 'Good school found.')
        elif school_vote == Vote.reject:
            return self._action(SwipeAction.nope, 'No good school found.')
        elif school_vote == Vote.no_info:
            return self._action(SwipeAction.nope, 'No school found.')
        elif school_vote == Vote.review:
            return self._action(SwipeAction.no_action, 'Unknown school found.')

    def _action(self, action: SwipeAction, reason: str):
        Logger.log(f'Action: {action.value}. Reason: {reason}', level=1)
        return action


if __name__ == '__main__':
    Logger.max_level = 3
    ProfileJudge().like_or_nope(TinderUser({
        'name': 'Tessa', 'distance_mi': 120, 'birth_date': '1986-04-03T00:00:00.000Z',
        'schools': [{'name': 'PABO Amsterdam'}, {'name': 'MBO Amsterdam'}]
    }))
