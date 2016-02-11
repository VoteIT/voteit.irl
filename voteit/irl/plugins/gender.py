from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import UserSchema
import colander
import deform

from voteit.irl import _
from voteit.irl.models.participant_number_ap import ParticipantNumberAP
from voteit.irl.schemas import ClaimParticipantNumberSchema


GENDER_VALUES = (('female', _(u"Female")),
                 ('male', _(u"Male")),
                 ('other', _(u"Other")))


class ParticipantNumberAPWithGender(ParticipantNumberAP):
    name = u"participant_number_ap_with_gender"
    title = _(u"Participant number registration with gender")
    description = _(u"participant_number_ap_with_gender_required_description",
                    default = u"Same as participant number, but this also requires gender to be specified.")

    def handle_success(self, view, appstruct):
        if 'gender' in appstruct:
            user = view.root['users'][view.request.authenticated_userid]
            user.set_field_value('gender', appstruct['gender'])
        return super(ParticipantNumberAPWithGender, self).handle_success(view, appstruct)


def add_gender_in_profile(schema, event):
    if event.context.type_name == 'Meeting' and \
        event.context.access_policy != ParticipantNumberAPWithGender.name:
        return #Skip in meeting context without this AP
    schema.add(colander.SchemaNode(colander.String(),
                                   name = "gender",
                                   title = _(u"Gender"),
                                   description = _(u"Used for statistics and perhaps gender based quotas. See meeting for details."),
                                   widget = deform.widget.RadioChoiceWidget(values = GENDER_VALUES)),)


def includeme(config):
    config.add_subscriber(add_gender_in_profile, [ClaimParticipantNumberSchema, ISchemaCreatedEvent])
    config.add_subscriber(add_gender_in_profile, [UserSchema, ISchemaCreatedEvent])
    config.registry.registerAdapter(ParticipantNumberAPWithGender, name = ParticipantNumberAPWithGender.name)
    #Maybe add attribute to User class
    from voteit.core.models.user import User
    if not hasattr(User, 'gender'):
        def _get(self):
            return self.get_field_value('gender', '')
        def _set(self, value):
            self.set_field_value('gender', value)
        User.gender = property(_get, _set)
