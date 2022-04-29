from ProfileJudge.vote import Vote
from logger import Logger


class VoteLoggerMixin:
    def _vote(self, info: str, vote: Vote, reason: str):
        Logger.log(f'{info}. Vote: {vote.value}. Reason: {reason}.', level=2)
        return vote
