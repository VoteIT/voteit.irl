# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import SiteSettingsSchema
from arche.schemas import UserSchema
import colander
import deform
from voteit.core.models.interfaces import IMeeting

from voteit.irl import _
from voteit.irl.models.participant_number_ap import ParticipantNumberAP
from voteit.irl.schemas import ClaimParticipantNumberSchema


PRONOUN_VALUES = (('she', _('She')),
                  ('he', _('He')),
                  ('ze', _('Ze')))
PRONOUN_NAME_DICT = dict(PRONOUN_VALUES)
PRONOUN_NAME_DICT[''] = _('Unknown')
GENDER_VALUES = (('female', _("Female")),
                 ('male', _("Male")),
                 ('other', _("Other")))
GENDER_NAME_DICT = dict(GENDER_VALUES)
GENDER_NAME_DICT[''] = _('Unknown')

GENDER_DISPLAY_TYPES = (
    ("", _("Don't display")),
    ("gender", _("Gender")),
    ("pronoun", _("Pronoun")),
)


class GenderStatistics(object):
    def __init__(self):
        self.results = dict((g[0], Decimal(0)) for g in GENDER_VALUES)
        self.results[''] = 0  # Unknown

    def add(self, gender, amount):
        self.results[gender] += amount

    @property
    def total(self):
        return sum(self.results.values())

    @property
    def sums(self):
        class Sums(object):
            def __init__(self, gender, results, total):
                self.gender = gender
                self.percentage = results[gender] / total * 100
                self.sum = results[gender]
                self.name = GENDER_NAME_DICT.get(gender)

        total = self.total
        return sorted([Sums(g, self.results, total) for g in self.results.keys() if self.results[g]],
                      key=lambda s: s.gender)


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


def add_gender_in_schema(schema, event):
    schema.add(colander.SchemaNode(
        colander.String(),
        name="gender",
        title=_("Gender"),
        description=_("Used for statistics and perhaps gender based quotas. See meeting for details."),
        missing="",
        widget=deform.widget.RadioChoiceWidget(values=GENDER_VALUES)),
    )
    request = getattr(event, 'request', None)
    if request.root.site_settings.get('pronoun_active'):
        schema.add(colander.SchemaNode(
            colander.String(),
            name="pronoun",
            title=_("Pronoun"),
            description=_("Shown in speaker lists."),
            missing="",
            widget=deform.widget.RadioChoiceWidget(values=PRONOUN_VALUES)),
        )


def pronoun_in_site_settings(schema, event):
    schema.add(colander.SchemaNode(
        colander.Boolean(),
        name="pronoun_active",
        title=_("Let users select pronoun"),
        description=_("Pronoun might be shown in different contexts like the speaker list."),
        missing=False))


def add_gender_in_meeting(schema, event):
    context = getattr(event, 'context', None)
    if not IMeeting.providedBy(context):
        return
    if context.type_name == 'Meeting' and context.access_policy == ParticipantNumberAPWithGender.name:
        add_gender_in_schema(schema, event)


def add_show_gender_in_speaker_list(schema, event):
    """ This will only be activated if voteit.debate is detected on include."""
    schema.add(colander.SchemaNode(
        colander.String(),
        name="show_gender_in_speaker_list",
        title=_("Show gender in speaker lists?"),
        description=_("It will only work if the chosen speaker list system supports this."),
        missing="",
        widget=deform.widget.RadioChoiceWidget(values=GENDER_DISPLAY_TYPES)),
    )


def includeme(config):
    config.add_subscriber(add_gender_in_meeting, [ClaimParticipantNumberSchema, ISchemaCreatedEvent])
    config.add_subscriber(add_gender_in_schema, [UserSchema, ISchemaCreatedEvent])
    config.add_subscriber(pronoun_in_site_settings, [SiteSettingsSchema, ISchemaCreatedEvent])
    config.registry.registerAdapter(ParticipantNumberAPWithGender, name=ParticipantNumberAPWithGender.name)
    # Add attribute to User class
    from voteit.core.models.user import User
    User.add_field('gender')
    User.add_field('pronoun')

    try:
        from voteit.debate.schemas import SpeakerListSettingsSchema
        include_show_gender = True
    except ImportError:
        # Skipping inclusion
        include_show_gender = False
    if include_show_gender:
        config.add_subscriber(add_show_gender_in_speaker_list, [SpeakerListSettingsSchema, ISchemaCreatedEvent])
