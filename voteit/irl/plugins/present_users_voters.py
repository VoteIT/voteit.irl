from voteit.core.models.interfaces import IMeeting

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IMeetingPresence
from voteit.irl.models.elegible_voters_method import ElegibleVotersMethod

class MakePresentUsersVoters(ElegibleVotersMethod):
    name = u'present_users_voters'
    title = _(u"Set present users as voters")
    description = _(u"Will remove voting permission for anyone not set as present.")

    def get_voters(self, **kw):
        request = kw['request']
        context = kw['context']
        meeting_presence = request.registry.getAdapter(context, IMeetingPresence)
        return frozenset(meeting_presence.present_userids)


def includeme(config):
    config.registry.registerAdapter(MakePresentUsersVoters, (IMeeting,), name = MakePresentUsersVoters.name)
