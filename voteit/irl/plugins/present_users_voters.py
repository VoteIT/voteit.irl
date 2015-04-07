from __future__ import unicode_literals

from voteit.core.models.interfaces import IMeeting

from voteit.irl import _
from voteit.irl.models.elegible_voters_method import ElegibleVotersMethod
from voteit.irl.models.interfaces import IMeetingPresence


class MakePresentUsersVoters(ElegibleVotersMethod):
    name = 'present_users_voters'
    title = _("Set present users as voters")
    description = _("Will remove voting permission for anyone not set as present.")

    def get_voters(self, request = None, **kw):
        meeting_presence = request.registry.getAdapter(self.context, IMeetingPresence)
        return frozenset(meeting_presence.present_userids)


def includeme(config):
    config.registry.registerAdapter(MakePresentUsersVoters, name = MakePresentUsersVoters.name)
