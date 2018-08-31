from __future__ import unicode_literals

import colander
from arche.interfaces import ISchemaCreatedEvent
from pyramid.threadlocal import get_current_request
from voteit.core.views.control_panel import control_panel_link

from voteit.irl import _
from voteit.irl.models.elegible_voters_method import ElegibleVotersMethod
from voteit.irl.models.interfaces import IMeetingPresence
from voteit.irl.models.interfaces import IParticipantNumbers


class MakePresentUsersVoters(ElegibleVotersMethod):
    name = 'present_with_pn_voters'
    title = _("Present with participant number in set range")
    description = _("present_with_pn_voters_description",
                    default="Will remove voting permission for anyone not set as present. "
                            "Users without a participant number will be ignored, or if "
                            "they're outside of the setting. (See the control panel)")

    def get_voters(self, request=None, **kw):
        if request is None:
            request = get_current_request()
        meeting_presence = request.registry.getAdapter(self.context, IMeetingPresence)
        participant_numbers = request.registry.getAdapter(self.context, IParticipantNumbers)
        results = set()
        valid_range = get_valid_range(self.context)
        for userid in meeting_presence.present_userids:
            if userid in participant_numbers.userid_to_number:
                if valid_range:
                    num = participant_numbers.userid_to_number.get(userid, None)
                    if num is not None and num >= valid_range[0] and num <= valid_range[1]:
                        results.add(userid)
                else:
                    results.add(userid)
        return frozenset(results)


class ElegibleVoterPNRangeValidator(object):

    def __call__(self, node, value):
        parts = value.split('-')
        err = _("Must be written as 'NN-XX' where N is low nr and X high.")
        if len(parts) != 2:
            raise colander.Invalid(node, err)
        try:
            parts = [int(x) for x in parts]
        except:
            raise colander.Invalid(node, err)
        if parts[0] >= parts[1]:
            raise colander.Invalid(node, _("First value must be higher than second"))


def inject_in_settings(schema, event):
    schema.add(
        colander.SchemaNode(
            colander.String(),
            title = _("Voter participant number range"),
            description=_("voter_pn_range_desc",
                          default="Write number as 'NN-NN', i.e. 10-20 means that "
                                  "10 to and including 20 will be voters if they're "
                                  "marked as present."),
            name = 'elegible_voter_pn',
            missing = "",
            validator = ElegibleVoterPNRangeValidator(),
        )
    )


def get_valid_range(meeting):
    val = getattr(meeting, 'elegible_voter_pn', None)
    if val is None:
        return
    parts = val.split('-')
    try:
        return [int(parts[0]), int(parts[1])]
    except:
        pass


def includeme(config):
    config.registry.registerAdapter(MakePresentUsersVoters, name=MakePresentUsersVoters.name)
    # Schema
    from voteit.irl.schemas import MeetingPresenceSettingsSchema
    config.add_subscriber(inject_in_settings, [MeetingPresenceSettingsSchema, ISchemaCreatedEvent])
    # Add properties
    from voteit.irl.models.meeting_presence import MeetingPresence
    MeetingPresence.elegible_voter_pn = ""
