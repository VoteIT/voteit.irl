from __future__ import unicode_literals

from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree
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

    def __init__(self, context):
        self.context = context

    @property
    def open(self):
        return bool(self.start_time)

    @property
    def present_userids(self):
        try:
            return self.context._meeting_presence_userids
        except AttributeError:
            self.context._meeting_presence_userids = OOSet()
            return self.context._meeting_presence_userids

    @property
    def enabled(self):
        return getattr(self.context, '_meeting_presence_enabled', None)
    @enabled.setter
    def enabled(self, value):
        self.context._meeting_presence_enabled = value

    @property
    def start_time(self):
        return getattr(self.context, '_v_meeting_presence_start_time', None)
    @start_time.setter
    def start_time(self, value):
        self.context._v_meeting_presence_start_time = value
    @start_time.deleter
    def start_time(self):
        delattr(self.context, '_v_meeting_presence_start_time')

    @property
    def archive(self):
        try:
            return self.context._meeting_presence_archive
        except AttributeError:
            self.context._meeting_presence_archive = IOBTree()
            return self.context._meeting_presence_archive

    def start_check(self):
        self.present_userids.clear()
        self.start_time = utcnow()

    def end_check(self):
        self.archive_current()

    def add(self, userid):
        if not self.open:
            raise HTTPForbidden(_("Meeting presence check isn't open"))
        assert isinstance(userid, basestring)
        self.present_userids.add(userid)

    def remove(self, userid):
        if not self.open:
            raise HTTPForbidden(_("Meeting presence check isn't open"))
        assert isinstance(userid, basestring)
        self.present_userids.remove(userid)

    def archive_current(self):
        if self.open:
            try:
                next_key = self.archive.maxKey() + 1
            except ValueError:
                next_key = 1
            self.archive[next_key] = OOBTree(
                present_userids = frozenset(self.present_userids),
                start_time = self.start_time,
                end_time = utcnow(),
            )
            del self.start_time
        else: #pragma: no coverage
            raise ValueError("Check not open, no archive can be created")

    def __contains__(self, val):
        return val in self.present_userids


def includeme(config):
    config.registry.registerAdapter(MeetingPresence)
