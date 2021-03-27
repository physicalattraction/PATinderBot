from ProfileJudge.school_manager import SchoolManager
from ProfileJudge.word_manager import ACTION_REQUIRED, APPROVED
from enums import SwipeAction
from tinder_user import TinderUser


class ProfileJudge:
    """
    Class responsible for determining the swipe action for a given user
    """

    def __init__(self):
        self.school_manager = SchoolManager()

    def like_or_nope(self, user: TinderUser) -> SwipeAction:
        """
        Determine the SwipeAction for the given user

        If there is at least one good school: like
        If not, if there is at least one unknown school: no_action
        If not: nope

        # TODO: Check for bio
        """

        # Check for distance in km
        if user.distance < 20:
            # If less than 20 km, I want to check them out manually
            print(f'To check out manually: {user}')
            return SwipeAction.no_action
        elif user.distance > 200:
            # If outside The Netherlands, automatic reject
            print(f'Distance too large for: {user}')
            return SwipeAction.nope

        # Check for schools the user went to. If she went to one of the approved schools,
        # it's an automatic like. If there is at least unknown school, no action is taken,
        # but the Bot user shall qualify the school in the schools file. If all schools are
        # rejected, the user is rejected.
        statuses = [self.school_manager.get_status(school) for school in user.schools]
        if APPROVED in statuses:
            print(f'Good school for {user}: {user.schools}. Action: {SwipeAction.like.value}')
            return SwipeAction.like
        elif ACTION_REQUIRED in statuses:
            print(f'Unknown school for {user}: {user.schools}. Action: {SwipeAction.no_action.value}')
            return SwipeAction.no_action
        else:
            # TODO: Fallthrough for when there is no school
            print(f'No good school for {user}: {user.schools}. Action: {SwipeAction.nope.value}')
            return SwipeAction.nope
