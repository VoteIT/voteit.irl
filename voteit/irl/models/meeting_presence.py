from __future__ import unicode_literals

from BTrees.OOBTree import OOSet
from arche.utils import utcnow
from pyramid.httpexceptions import HTTPForbidden
from voteit.core.models.interfaces import IMeeting
from zope.component import adapter
from zope.interface import implementer

from voteit.irl import _
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

    @property
    def open(self):
        return getattr(self.context, '__meeting_presence_open__', False)
    @open.setter
    def open(self, value):
        assert isinstance(value, bool)
        self.context.__meeting_presence_open__ = value

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

    def __contains__(self, val):
        return val in self.present_userids


def includeme(config):
    config.registry.registerAdapter(MeetingPresence)
