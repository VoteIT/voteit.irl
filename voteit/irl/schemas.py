import colander
import deform
from betahaus.pyracont.decorators import schema_factory

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


@schema_factory('ClaimParticipantNumber')
class ClaimParticipantNumberSchema(colander.Schema):
    token = colander.SchemaNode(colander.String(),
                                validator = deferred_participant_number_token_validator,
                                title = _(u"Participant code"),
                                description = _(u"enter_token_description",
                                                default = u"Enter the code sent to you. It will have the format xxxx-xxxx. "
                                                          u"Note that it's case sensitive and can only be used once."))
