from pyramid.httpexceptions import HTTPFound
from voteit.core.models.access_policy import AccessPolicy

from voteit.irl.models.interfaces import IParticipantNumbers
from voteit.irl import _
from voteit.irl.schemas import ClaimParticipantNumberSchema
from voteit.irl.schemas import ConfigureParticipantNumberAP


class ParticipantNumberAP(AccessPolicy):
    name = "participant_number_ap"
    title = _("Participant number registration")
    description = _("participant_number_ap_description",
                    default = "If participant numbers are enabled for this meeting, use this policy "
                    "to allow meeting access through registration of a participant number.")

    def schema(self):
        schema = ClaimParticipantNumberSchema()
        if self.context.get_field_value('pn_ap_public_roles', False):
            schema['token'].missing = u""
            schema['token'].description = _(u"token_validator_description_when_ok_without",
                                            default = u"Enter your code to claim your participant number and all permissions associated with it. "
                                                u"If you're not supposed to have a participant number, you're allowed to proceed by clicking "
                                                u"'Request access'.")
        return schema

    def handle_success(self, view, appstruct):
        public_roles = self.context.get_field_value('pn_ap_public_roles', False)
        userid = view.request.authenticated_userid
        if appstruct['token']:
            #The schema validated the token if it existed
            claimed_roles = self.context.get_field_value('pn_ap_claimed_roles', ())
            if claimed_roles:
                self.context.add_groups(userid, claimed_roles)
            participant_numbers = view.request.registry.getAdapter(self.context, IParticipantNumbers)
            number = participant_numbers.claim_ticket(userid, appstruct['token'])
            msg = _(u"number_now_assigned_notice",
                    default = u"You're now assigned number ${number}.",
                    mapping = {'number': number})
            view.flash_messages.add(msg)
        elif public_roles:
            self.context.add_groups(userid, public_roles)
            msg = _(u"access_without_pn_notice",
                    default = u"You've been given access to the meeting without a participant number.")
            view.flash_messages.add(msg)
        return HTTPFound(location = view.request.resource_url(self.context)) #Will raise unauthorized if nothing was done

    def config_schema(self):
        return ConfigureParticipantNumberAP()


def includeme(config):
    config.registry.registerAdapter(ParticipantNumberAP, name = ParticipantNumberAP.name)
