from betahaus.pyracont.factories import createSchema
from voteit.core.models.access_policy import AccessPolicy
from pyramid.httpexceptions import HTTPFound

from voteit.irl.models.interfaces import IParticipantNumbers
from voteit.irl import VoteIT_IRL_MF as _


class ParticipantNumberAP(AccessPolicy):
    name = u"participant_number_ap"
    title = _(u"Participant number registration")
    description = _(u"participant_number_ap_description",
                    default = u"If participant numbers are enabled for this meeting, use this policy "
                        u"to allow meeting access through registration of a participant number.")
    configurable = True

    def schema(self, api):
        schema = createSchema("ClaimParticipantNumber")
        if self.context.get_field_value('pn_ap_public_roles', False):
            schema['token'].missing = u""
            schema['token'].description = _(u"token_validator_description_when_ok_without",
                                            default = u"Enter your code to claim your participant number and all permissions associated with it. "
                                                u"If you're not supposed to have a participant number, you're allowed to proceed by clicking "
                                                u"'Request access'.")
        return schema

    def handle_success(self, api, appstruct):
        public_roles = self.context.get_field_value('pn_ap_public_roles', False)
        if appstruct['token']:
            #The schema validated the token if it existed
            claimed_roles = api.meeting.get_field_value('pn_ap_claimed_roles', ())
            if claimed_roles:
                api.meeting.add_groups(api.userid, claimed_roles)
            participant_numbers = api.request.registry.getAdapter(api.meeting, IParticipantNumbers)
            number = participant_numbers.claim_ticket(api.userid, appstruct['token'])
            msg = _(u"number_now_assigned_notice",
                    default = u"You're now assigned number ${number}.",
                    mapping = {'number': number})
            api.flash_messages.add(msg)
        elif public_roles:
            api.meeting.add_groups(api.userid, public_roles)
            msg = _(u"access_without_pn_notice",
                    default = u"You've been given access to the meeting without a participant number.")
            api.flash_messages.add(msg)
        return HTTPFound(location = api.request.resource_url(api.meeting)) #Will raise unauthorized if nothing was done

    def config_schema(self, api):
        return createSchema("ConfigureParticipantNumberAP")


def includeme(config):
    config.registry.registerAdapter(ParticipantNumberAP, name = ParticipantNumberAP.name)
