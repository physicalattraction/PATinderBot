from enum import Enum


class Vote(Enum):
    approve = 'approve'
    reject = 'reject'
    no_info = 'no info'
    review = 'review'