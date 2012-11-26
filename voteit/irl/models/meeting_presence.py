from zope.interface import implements
from BTrees.OOBTree import OOSet

from voteit.core.models.date_time_util import utcnow
from pyramid.httpexceptions import HTTPForbidden

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IMeetingPresence


class MeetingPresence(object):
    __doc__ = IMeetingPresence.__doc__
    implements(IMeetingPresence)
    open = None
    start_time = None
    end_time = None

    def __init__(self):
        self.open = False
        self.present_userids = OOSet()

    def start_check(self):
        self.open = True
        self.present_userids.clear()
        self.start_time = utcnow()
        self.end_time = None

    def end_check(self):
        self.open = False
        self.end_time = utcnow()

    def add(self, userid):
        if not self.open:
            raise HTTPForbidden(_(u"Meeting presence check isn't open"))
        assert isinstance(userid, basestring)
        self.present_userids.add(userid)
