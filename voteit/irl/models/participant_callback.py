from __future__ import unicode_literals

from BTrees.IOBTree import IOBTree
from arche.interfaces import IFlashMessages
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_request
from six import string_types
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from zope.component import adapter
from zope.interface import implementer

from voteit.irl import _
from voteit.irl.models.interfaces import IParticipantCallback
from voteit.irl.models.interfaces import IParticipantCallbacks
from voteit.irl.models.interfaces import IParticipantNumbers


@implementer(IParticipantCallbacks)
@adapter(IMeeting)
class ParticipantCallbacks(object):

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
        if number in self.callbacks:
            return self.callbacks[number]
        return []

    def execute_callbacks_for(self, number, userid, limit = None, request = None, **kw):
        assert isinstance(number, int)
        assert isinstance(userid, string_types)
        if request is None:
            request = get_current_request()
        if isinstance(limit, string_types):
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
            msg = _("could_not_execute_callback_error",
                    default = "Some callbacks for the UserId '${userid}' failed. Contact the moderator about this. "
                              "The ones that failed were: ${callback_errors}",
                    mapping = {'callback_errors': ", ".join(errors), 'userid': userid})
            fm.add(msg, type = 'danger', require_commit = False)
        return executed

    def add(self, callback, start, end = None):
        assert isinstance(callback, string_types)
        if end == None:
            end = start
        assert start <= end
        added = []
        existed = []
        for i in range(start, end + 1): #Since end should be included.
            if i not in self.callbacks:
                self.callbacks[i] = PersistentList()
            callbacks = self.callbacks[i]
            if callback not in callbacks:
                callbacks.append(callback)
                added.append(i)
            else:
                existed.append(i)
        return added, existed

    def remove(self, callback, start, end = None):
        assert isinstance(callback, string_types)
        if end == None:
            end = start
        assert start <= end, "Can't end before start"
        removed = []
        nonexistent = []
        for i in range(start, end + 1): #End value should be included
            callbacks = self.get_callbacks(i)
            if callback in callbacks:
                callbacks.remove(callback)
                removed.append(i)
            else:
                nonexistent.append(i)
        return removed, nonexistent


@implementer(IParticipantCallback)
@adapter(IMeeting)
class ParticipantCallback(object):
    """ Abstract class, see IParticipantCallback
    """
    name = ""
    title = ""
    description = ""
    
    def __init__(self, context):
        self.context = context

    def __call__(self, number, userid, **kw):
        raise NotImplementedError("Must be implemented by subclass")


class AssignVoterRole(ParticipantCallback):
    name = "allow_vote"
    title = _("Allow to vote")

    def __call__(self, number, userid, **kw):
        self.context.add_groups(userid, [security.ROLE_VOTER])


class AssignDiscussionRole(ParticipantCallback):
    name = "allow_discuss"
    title = _("Allow to discuss")

    def __call__(self, number, userid, **kw):
        self.context.add_groups(userid, [security.ROLE_DISCUSS])


class AssignProposeRole(ParticipantCallback):
    name = "allow_propose"
    title = _("Allow to propose")

    def __call__(self, number, userid, **kw):
        self.context.add_groups(userid, [security.ROLE_PROPOSE])


def includeme(config):
    config.registry.registerAdapter(ParticipantCallbacks)
    config.registry.registerAdapter(AssignVoterRole, name = AssignVoterRole.name)
    config.registry.registerAdapter(AssignDiscussionRole, name = AssignDiscussionRole.name)
    config.registry.registerAdapter(AssignProposeRole, name = AssignProposeRole.name)
