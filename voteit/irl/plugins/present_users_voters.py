from __future__ import unicode_literals

import colander
from arche.interfaces import ISchemaCreatedEvent
from pyramid.threadlocal import get_current_request

from voteit.irl import _
from voteit.irl.models.elegible_voters_method import ElegibleVotersMethod
from voteit.irl.models.interfaces import IMeetingPresence
from voteit.irl.models.interfaces import IParticipantNumbers


class MakePresentUsersVoters(ElegibleVotersMethod):
    name = 'present_with_pn_voters'
    title = _("Present with participant number (set on meeting -> advanced tab)")
    description = _("present_with_pn_voters_description",
                    default = "Will remove voting permission for anyone not set as present. "
                    "Users without a participant number will be ignored, or if they're outside of the meeting setting.")

    def get_voters(self, request = None, **kw):
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
        for x in parts:
            try:
                int(x)
            except:
                raise colander.Invalid(node, err)
        if parts[0] >= parts[1]:
            raise colander.Invalid(node, _("First value must be higher than second"))


def inject_in_meeting_schema(schema, event):
    schema.add(
        colander.SchemaNode(
            colander.String(),
            title = _("Voter participant number range"),
            description = _("voter_pn_range_desc",
                            default = "Anyone with a participant number will be able to "
                                      "become a voter during a meeting presence check. "
                                      "Write number as 'NN-NN', i.e. 10-20 means that "
                                      "10 to and including 20 will be voters."),
            name = 'elegible_voter_pn',
            missing = "",
            validator = ElegibleVoterPNRangeValidator(),
            tab='advanced',
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
    config.registry.registerAdapter(MakePresentUsersVoters, name = MakePresentUsersVoters.name)
    #Add subscriber for schema
    from voteit.core.schemas.meeting import EditMeetingSchema
    config.add_subscriber(inject_in_meeting_schema, [EditMeetingSchema, ISchemaCreatedEvent])
    #Add properties
    from voteit.core.models.meeting import Meeting
    Meeting.elegible_voter_pn = ""
