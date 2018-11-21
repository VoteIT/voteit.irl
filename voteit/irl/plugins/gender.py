# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
import json

from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import SiteSettingsSchema
from arche.schemas import UserSchema
import colander
import deform
from arche.views.base import BaseForm
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config

from voteit.core.models.interfaces import (
    IMeeting,
    IUser,
)

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
        widget=deform.widget.RadioChoiceWidget(values=GENDER_VALUES)),
    )
    request = getattr(event, 'request', None)
    if request.root.site_settings.get('pronoun_active'):
        schema.add(colander.SchemaNode(
            colander.String(),
            name="pronoun",
            title=_("Pronoun"),
            description=_("Shown in speaker lists."),
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


def add_gender_in_speaker_list(schema, event):
    schema.description = _('You have to select gender to join a speaker list.')
    add_gender_in_schema(schema, event)


def add_gender_in_speaker_list_settings(schema, event):
    request = event.request
    if request.root.site_settings.get('pronoun_active'):
        title = _('Show gender or pronoun in speaker lists')
        values = (('', _('No')), ('gender', _('Gender')), ('pronoun', _('Pronoun')))
    else:
        title = _('Show gender in speaker lists')
        values = (('', _('No')), ('gender', _('Yes')))
    schema.add(colander.SchemaNode(
        colander.String(),
        name='show_gender_in_speaker_list',
        tab=request.localizer.translate(_('Gender')),
        title=title,
        widget=deform.widget.RadioChoiceWidget(values=values),
        default='',
        missing='',
    ))
    schema.add(colander.SchemaNode(
        colander.Boolean(),
        name='require_gender_in_speaker_list',
        tab=request.localizer.translate(_('Gender')),
        title=_('Require gender to join speaker list'),
        description=_('Users will have to select gender to be able to join a speaker list.'),
        default=False,
        missing=False,
    ))


@view_config(context=IUser, name='gender_settings', renderer='arche:templates/form.pt')
class GenderSettingsForm(BaseForm):
    schema_name = 'user_join_speaker_list'
    type_name = 'SpeakerLists'
    title = _("Gender settings")
    formid = 'user_join_speaker_list'
    use_ajax = True

    def _remove_modal_response(self, appstruct=None, value=None):
        data = value is not None and {'callback_value': json.dumps(value)} or {}
        return Response(render("arche:templates/deform/destroy_modal.pt", data, request=self.request))

    cancel_success = cancel_failure = _remove_modal_response

    def save_success(self, appstruct):
        self.context.update(**appstruct)
        return self._remove_modal_response(value='resolve')


def includeme(config):
    config.add_subscriber(add_gender_in_meeting, [ClaimParticipantNumberSchema, ISchemaCreatedEvent])
    config.add_subscriber(add_gender_in_schema, [UserSchema, ISchemaCreatedEvent])
    config.add_subscriber(pronoun_in_site_settings, [SiteSettingsSchema, ISchemaCreatedEvent])
    try:
        from voteit.debate.schemas import (
            UserJoinSpeakerList,
            SpeakerListSettingsSchema,
        )
        config.add_subscriber(add_gender_in_speaker_list, [UserJoinSpeakerList, ISchemaCreatedEvent])
        config.add_subscriber(add_gender_in_speaker_list_settings, [SpeakerListSettingsSchema, ISchemaCreatedEvent])
    except ImportError:
        pass
    config.registry.registerAdapter(ParticipantNumberAPWithGender, name=ParticipantNumberAPWithGender.name)
    # Add attribute to User class
    from voteit.core.models.user import User
    User.add_field('gender')
    User.add_field('pronoun')
    config.scan(__name__)
