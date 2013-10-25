from BTrees.IOBTree import IOBTree
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_request
from zope.component import adapts
from zope.interface import implements
from voteit.core.models.interfaces import IMeeting
from voteit.core import security
from voteit.core.models.interfaces import IFlashMessages

from .interfaces import IParticipantCallback
from .interfaces import IParticipantCallbacks
from .interfaces import IParticipantNumbers
from voteit.irl import VoteIT_IRL_MF as _


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

    def execute_callbacks_for(self, number, userid, limit = None, request = None, **kw):
        assert isinstance(number, int)
        assert isinstance(userid, basestring)
        if request is None:
            request = get_current_request()
        if isinstance(limit, basestring):
            limit = (limit,)
        errors = []
        executed = []
        for callback_name in self.get_callbacks(number):
            if limit is None:
                callback = request.registry.queryAdapter(self.context, IParticipantCallback, name = callback_name)
            else:
                if not callback_name in limit:
                    continue
                callback = request.registry.queryAdapter(self.context, IParticipantCallback, name = callback_name)
            #Check that adapter was found
            if callback is None:
                errors.append(callback_name)
            else:
                callback(number, userid, request = request, **kw)
                executed.append(callback_name)
        if errors:
            fm = request.registry.getAdapter(request, IFlashMessages)
            msg = _(u"could_not_execute_callback_error",
                    default = u"Some callbacks for the UserId '${userid}' failed. Contact the moderator about this. "
                              u"The ones that failed were: ${callback_errors}",
                    mapping = {'callback_errors': ", ".join(errors), 'userid': userid})
            fm.add(msg, type = 'error')
        return executed

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


class ParticipantCallback(object):
    implements(IParticipantCallback)
    adapts(IMeeting)
    name = u""
    title = u""
    description = u""
    
    def __init__(self, context):
        self.context = context

    def __call__(self, number, userid, **kw):
        raise NotImplementedError("Must be implemented by subclass")


class AssignVoterRole(ParticipantCallback):
    name = u"allow_vote"
    title = _(u"Allow to vote")

    def __call__(self, number, userid, **kw):
        self.context.add_groups(userid, [security.ROLE_VOTER])


class AssignDiscussionRole(ParticipantCallback):
    name = u"allow_discuss"
    title = _(u"Allow to discuss")

    def __call__(self, number, userid, **kw):
        self.context.add_groups(userid, [security.ROLE_DISCUSS])


class AssignProposeRole(ParticipantCallback):
    name = u"allow_propose"
    title = _(u"Allow to propose")

    def __call__(self, number, userid, **kw):
        self.context.add_groups(userid, [security.ROLE_PROPOSE])


def includeme(config):
    config.registry.registerAdapter(ParticipantCallbacks)
    config.registry.registerAdapter(AssignVoterRole, name = AssignVoterRole.name)
    config.registry.registerAdapter(AssignDiscussionRole, name = AssignDiscussionRole.name)
    config.registry.registerAdapter(AssignProposeRole, name = AssignProposeRole.name)
