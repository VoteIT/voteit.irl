import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from voteit.core.validators import deferred_existing_userid_validator
from voteit.core.schemas.common import deferred_autocompleting_userid_widget
from voteit.core import security

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElectoralRegister
from voteit.irl.models.interfaces import IElegibleVotersMethod
from voteit.irl.models.interfaces import IParticipantNumbers


@colander.deferred
def elegible_voters_method_choices_widget(node, kw):
    """ Create a widget where you can choose all selectable methods to adjust elegible voters. """
    context = kw['context']
    request = kw['request']
    method_choices = set()
    for (name, method) in request.registry.getAdapters([context], IElegibleVotersMethod):
        method_choices.add((name, method.title))
    return deform.widget.SelectWidget(values=method_choices)


@schema_factory('ElegibleVotersMethodSchema')
class ElegibleVotersMethodSchema(colander.Schema):
    method_name = colander.SchemaNode(colander.String(),
                                 title = _(u"elegible_voters_method_name", default=u"Method to select elegible voters"),
                                 description = _(u"elegible_voters_method_description",
                                                 default=u"It will modify the voting permissions accoring to it's specifications."),
                                 widget = elegible_voters_method_choices_widget,)


@colander.deferred
def register_diff_choices_widget(node, kw):
    context = kw['context']
    request = kw['request']
    api = kw['api']
    electoral_register = request.registry.getAdapter(context, IElectoralRegister)
    choices = []
    for id in sorted(electoral_register.registers.keys(), key=int, reverse=True):
        timestamp = api.dt_util.dt_format(electoral_register.registers[id]['time'])
        title = "%s: %s" % (id, timestamp)
        choices.append((id, title))
    return deform.widget.SelectWidget(values=choices)


@schema_factory('ElectoralRegisterDiff')
class ElectoralRegisterDiffSchema(colander.Schema):
    first = colander.SchemaNode(colander.Int(),
                                  title = _(u"First register"),
                                  widget = register_diff_choices_widget,
                                  )
    second = colander.SchemaNode(colander.Int(),
                                  title = _(u"Second register"),
                                  widget = register_diff_choices_widget,
                                  )


@colander.deferred
def deferred_participant_number_token_validator(node, kw):
    context = kw['context']
    request = kw['request']
    return PNTokenValidator(context, request)


class PNTokenValidator(object):
    """ For meetings """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, node, value):
        participant_numbers = self.request.registry.getAdapter(self.context, IParticipantNumbers)
        if value not in participant_numbers.token_to_number:
            raise colander.Invalid(node, _(u"No match - remember that it's case sensitive!"))
        number = participant_numbers.token_to_number[value]
        if participant_numbers.tickets[number].claimed:
            raise colander.Invalid(node, _(u"This number has already been claimed."))


@schema_factory('ClaimParticipantNumber')
class ClaimParticipantNumberSchema(colander.Schema):
    token = colander.SchemaNode(colander.String(),
                                validator = deferred_participant_number_token_validator,
                                title = _(u"Participant code"),
                                description = _(u"enter_token_description",
                                                default = u"Enter the code sent to you. It will have the format xxxx-xxxx. "
                                                          u"Note that it's case sensitive and can only be used once."))


@colander.deferred
def deferred_existing_participant_number_validator(node, kw):
    context = kw['api'].meeting
    request = kw['request']
    return ExistingParticipantNumberValidator(context, request)


class ExistingParticipantNumberValidator(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, node, value):
        pn = self.request.registry.getAdapter(self.context, IParticipantNumbers)
        if value not in pn.number_to_userid.keys():
            return colander.Invalid(node, _(u"Participant number not found"))


def _meeting_roles_minus_moderator():
    roles = dict(security.MEETING_ROLES)
    del roles[security.ROLE_MODERATOR]
    return roles.items()


@schema_factory('ConfigureParticipantNumberAP')
class ConfigureParticipantNumberAP(colander.Schema):
    pn_ap_claimed_roles = colander.SchemaNode(
        deform.Set(allow_empty = False),
        title = _(u"Anyone registering with participant number will be given these roles"),
        description = _(u"pn_ap_claimed_roles_description",
                        default = u"Picking at least one is required. "
                            u"Note that if you allow registration to be bypassed (see below) the roles "
                            u"specified here won't be added when a meeting number is claimed by someone who's already a part of the meeting."),
        default = [security.ROLE_VIEWER],
        widget = deform.widget.CheckboxChoiceWidget(values = _meeting_roles_minus_moderator()),
    )
    pn_ap_public_roles = colander.SchemaNode(
        deform.Set(allow_empty = True),
        title = (u"Allow bypass and give access to anyone?"),
        description = _(u"pn_ap_public_roles_description",
                        default = u"If anything is checked below, any user will be able to bypass the access form "
                        u"and immediately gain the roles checked. Some examples - for meetings that are: "
                        u"Closed: check nothing below. "
                        u"Viewable for anyone: check view permission"
                        u"Open for participation from anyone: check all"),
        widget = deform.widget.CheckboxChoiceWidget(values = _meeting_roles_minus_moderator()),
    )


@colander.deferred
def deferred_autocompleting_participant_number_widget(node, kw):
    meeting = kw['api'].meeting
    request = kw['request']
    pn = request.registry.getAdapter(meeting, IParticipantNumbers)
    choices = tuple(pn.number_to_userid.keys())
    return deform.widget.AutocompleteInputWidget(
        size=15,
        values = choices,
        min_length=1)

@colander.deferred
def deferred_pn_from_get(node, kw):
    request = kw['request']
    return int(request.GET['pn'])


@schema_factory('AssignParticipantNumber')
class AssignParticipantNumber(colander.Schema):
    userid = colander.SchemaNode(
        colander.String(),
        title = _(u"UserID"),
        validator = deferred_existing_userid_validator,
        widget = deferred_autocompleting_userid_widget,
    )
    pn = colander.SchemaNode(
        colander.Int(),
        widget = deform.widget.HiddenWidget(),
        default = deferred_pn_from_get,
    )
