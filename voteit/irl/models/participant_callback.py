from BTrees.IOBTree import IOBTree
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry
from zope.component import adapts
from zope.interface import implements
from voteit.core.models.interfaces import IMeeting
from voteit.core import security

from .interfaces import IParticipantCallback
from .interfaces import IParticipantCallbacks
from .interfaces import IParticipantNumbers


class ParticipantCallbacks(object):
    implements(IParticipantCallbacks)
    adapts(IMeeting)

    def __init__(self, context):
        self.context = context

    @property
    def callbacks(self):
        try:
            return self.context.__participant_callbacks__
        except AttributeError:
            self.context.__participant_callbacks__ = IOBTree()
            return self.context.__participant_callbacks__

    def get_callbacks(self, number):
        if number not in self.callbacks:
            self.callbacks[number] = PersistentList()
        return self.callbacks[number]

    def add(self, callback, start, end = None):
        assert isinstance(callback, basestring)
        if end == None:
            end = start
        assert start <= end
        added = []
        existed = []
        for i in range(start, end + 1): #Range  stops before end otherwise
            callbacks = self.get_callbacks(i)
            if callback not in callbacks:
                callbacks.append(callback)
                added.append(i)
            else:
                existed.append(i)
            #FIXME: If user existed, execute callback?
        return added, existed

    def remove(self, callback, start, end = None):
        assert isinstance(callback, basestring)
        if end == None:
            end = start
        assert start <= end
        removed = []
        nonexistent = []
        for i in range(start, end + 1): #Range  stops before end otherwise
            callbacks = self.get_callbacks(i)
            if callback in callbacks:
                callbacks.remove(callback)
                removed.append(i)
            else:
                nonexistent.append(i)
        return removed, nonexistent

#    def execute_for(self, number, userid = None):
#        reg = get_current_registry()
#        #FIXME: Log fails
#        for name in self.callbacks:
#            if number not in self.callbacks[name]:
#                continue
#            callback = reg.queryAdapter(self.context, IParticipantCallback)
#            if callback:
#                callback(number, userid)
            #else:
                #FIXME: log fail

#    def execute_if_exists(self, callback, start, end = None):
#        assert isinstance(callback, basestring)
#        if end == None:
#            end = start
#        assert start <= end
#        reg = get_current_registry()
#        participant_numbers = reg.getAdapter(self.context, IParticipantNumbers)
#        executed = 0
#        nonexistent = 0
#        for i in range(start, end + 1): #Range  stops before end otherwise
#            if i not in self.callbacks:
#                continue
#            if callback in self.callbacks[i]:
#                
#                self.callbacks[i].remove(callback)
#                removed += 1
#            else:
#                nonexistent += 1
#        return removed, nonexistent




class ParticipantCallback(object):
    implements(IParticipantCallback)
    adapts(IMeeting)
    name = u""
    title = u""
    description = u""
    
    def __init__(self, context):
        self.context = context

    def __call__(self, number, userid):
        raise NotImplementedError("Must be implemented by subclass")


class AssignVoterRole(ParticipantCallback):
    name = u"allow_vote"
    title = u"Give voter role"

    def __call__(self, number, userid):
        self.context.add_groups(userid, [security.ROLE_VOTER])


class AssignDiscussionRole(ParticipantCallback):
    name = u"allow_discuss"
    title = u"Give discuss role"

    def __call__(self, number, userid):
        self.context.add_groups(userid, [security.ROLE_DISCUSS])


class AssignProposeRole(ParticipantCallback):
    name = u"allow_propose"
    title = u"Give propose role"

    def __call__(self, number, userid):
        self.context.add_groups(userid, [security.ROLE_PROPOSE])


def includeme(config):
    config.registry.registerAdapter(ParticipantCallbacks)
    config.registry.registerAdapter(AssignVoterRole, name = AssignVoterRole.name)
    config.registry.registerAdapter(AssignDiscussionRole, name = AssignDiscussionRole.name)
    config.registry.registerAdapter(AssignProposeRole, name = AssignProposeRole.name)
