from __future__ import unicode_literals

from voteit.core.models.interfaces import IMeeting
from pyramid.threadlocal import get_current_request

from voteit.irl import _
from voteit.irl.models.elegible_voters_method import ElegibleVotersMethod
from voteit.irl.models.interfaces import IMeetingPresence
from voteit.irl.models.interfaces import IParticipantNumbers


class MakePresentUsersVoters(ElegibleVotersMethod):
    name = 'present_with_pn_voters'
    title = _("Present with participant number")
    description = _("present_with_pn_voters_description",
                    default = "Will remove voting permission for anyone not set as present. "
                    "Users without a participant number will be ignored.")

    def get_voters(self, request = None, **kw):
        if request is None:
            request = get_current_request()
        meeting_presence = request.registry.getAdapter(self.context, IMeetingPresence)
        participant_numbers = request.registry.getAdapter(self.context, IParticipantNumbers)
        results = set()
        for userid in meeting_presence.present_userids:
            if userid in participant_numbers.userid_to_number:
                results.add(userid)
        return frozenset(results)

def includeme(config):
    config.registry.registerAdapter(MakePresentUsersVoters, name = MakePresentUsersVoters.name)
