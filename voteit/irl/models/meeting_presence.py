from zope.interface import implementer
from zope.component import adapter
from BTrees.OOBTree import OOSet

from voteit.core.models.date_time_util import utcnow
from voteit.core.models.interfaces import IMeeting
from pyramid.httpexceptions import HTTPForbidden

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IMeetingPresence


@implementer(IMeetingPresence)
@adapter(IMeeting)
class MeetingPresence(object):
    __doc__ = IMeetingPresence.__doc__
    open = None
    start_time = None
    end_time = None

    def __init__(self, context):
        self.context = context

    def _get_open(self):
        return getattr(self.context, '__meeting_presence_open__', False)
    def _set_open(self, value):
        assert isinstance(value, bool)
        self.context.__meeting_presence_open__ = value
    open = property(_get_open, _set_open)

    @property
    def present_userids(self):
        try:
            return self.context.__meeting_presence_userids__
        except AttributeError:
            self.context.__meeting_presence_userids__ = OOSet()
            return self.context.__meeting_presence_userids__

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


def includeme(config):
    config.registry.registerAdapter(MeetingPresence)
