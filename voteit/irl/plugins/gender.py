import colander
import deform
from betahaus.pyracont.interfaces import ISchemaCreatedEvent
from voteit.core.schemas.interfaces import IEditUserSchema
from pyramid.threadlocal import get_current_request

from voteit.irl.interfaces import IClaimParticipantNumber
from voteit.irl.models.participant_number_ap import ParticipantNumberAP
from voteit.irl import VoteIT_IRL_MF as _


GENDER_VALUES = (('female', _(u"Female")),
                 ('male', _(u"Male")),
                 ('other', _(u"Other")))


class ParticipantNumberAPWithGender(ParticipantNumberAP):
    name = u"participant_number_ap_with_gender"
    title = _(u"Participant number registration with gender")
    description = _(u"participant_number_ap_with_gender_required_description",
                    default = u"Same as participant number, but this also requires gender to be specified.")

    def handle_success(self, api, appstruct):
        if 'gender' in appstruct:
            api.user_profile.set_field_value('gender', appstruct['gender'])
        return super(ParticipantNumberAPWithGender, self).handle_success(api, appstruct)


def add_gender_in_profile(schema, event):
    request = get_current_request()
    if request.context.content_type == 'Meeting' and \
        request.context.get_field_value('access_policy') != ParticipantNumberAPWithGender.name:
        return #Skip in meeting context without this AP
    schema.add(colander.SchemaNode(colander.String(),
                                   name = "gender",
                                   title = _(u"Gender"),
                                   description = _(u"Used for statistics and perhaps gender based quotas. See meeting for details."),
                                   widget = deform.widget.RadioChoiceWidget(values = GENDER_VALUES)),
                                   )


def includeme(config):
    config.add_subscriber(add_gender_in_profile, [IEditUserSchema, ISchemaCreatedEvent])
    config.add_subscriber(add_gender_in_profile, [IClaimParticipantNumber, ISchemaCreatedEvent])
    config.registry.registerAdapter(ParticipantNumberAPWithGender, name = ParticipantNumberAPWithGender.name)
