from betahaus.pyracont.factories import createSchema
from voteit.core.models.access_policy import AccessPolicy
from pyramid.httpexceptions import HTTPFound

from voteit.irl.models.interfaces import IParticipantNumbers
from voteit.irl import VoteIT_IRL_MF as _


class ParticipantNumberAP(AccessPolicy):
    name = u"participant_number_ap"
    title = _(u"Participant number registration")
    description = _(u"participant_number_ap_description",
                    default = u"If participant numbers are enabled and distributed for this meeting, use this policy "
                        u"to allow access through registration of one of those numbers.")
    configurable = False

    def __init__(self, context):
        self.context = context

    def schema(self, api):
        return createSchema("ClaimParticipantNumber")

    def handle_success(self, api, appstruct):
        participant_numbers = api.request.registry.getAdapter(api.meeting, IParticipantNumbers)
        number = participant_numbers.claim_ticket(api.userid, appstruct['token'])
        msg = _(u"number_now_assigned_notice",
                default = u"You're now assigned number ${number}.",
                mapping = {'number': number})
        api.flash_messages.add(msg)
        return HTTPFound(location = api.meeting_url)

    def config_schema(self, api):
        pass


def includeme(config):
    config.registry.registerAdapter(ParticipantNumberAP, name = ParticipantNumberAP.name)
