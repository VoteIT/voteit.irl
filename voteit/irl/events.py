from zope.interface import implements

from .interfaces import IParticipantNumberClaimed


class ParticipantNumberClaimed(object):
    implements(IParticipantNumberClaimed)

    def __init__(self, meeting, number, userid):
        self.meeting = meeting
        self.number = number
        self.userid = userid
