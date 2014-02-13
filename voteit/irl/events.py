from zope.interface import implementer

from .interfaces import IParticipantNumberClaimed


@implementer(IParticipantNumberClaimed)
class ParticipantNumberClaimed(object):

    def __init__(self, meeting, number, userid):
        self.meeting = meeting
        self.number = number
        self.userid = userid
