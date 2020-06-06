from enum import Enum


class SwipeAction(Enum):
    like = 'like'
    nope = 'nope'
    no_action = 'no_action'


class Status(Enum):
    liked = 'liked'
    noped = 'noped'
    matched = 'matched'
