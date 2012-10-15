import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from pyramid.traversal import find_interface

from voteit.core.models.interfaces import IMeeting
from voteit.core.security import context_effective_principals
from voteit.core.security import ROLE_VIEWER
from voteit.core.security import VIEW
from voteit.core.security import find_authorized_userids

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElectoralRegisterMethod
from voteit.irl.models.interfaces import IElectoralRegister


@colander.deferred
def deferred_viewer_userid_validator(node, kw):
    context = kw['context']
    return ViewerUserId(context)

class ViewerUserId(object):
    def __init__(self, context):
        self.context = context
    
    def __call__(self, node, value):
        meeting = find_interface(self.context, IMeeting)
        assert meeting
        if ROLE_VIEWER not in context_effective_principals(meeting, value):
            msg = _(u"User must have at least view permission")
            raise colander.Invalid(node, msg)

@colander.deferred
def deferred_autocompleting_viewer_userid_widget(node, kw):
    context = kw['context']
    meeting = find_interface(context, IMeeting)
    assert meeting
    choices = tuple(find_authorized_userids(meeting, (VIEW, )))
    return deform.widget.AutocompleteInputWidget(
        size=15,
        values = choices,
        min_length=1)
    
@colander.deferred
def electoral_register_method_choices_widget(node, kw):
    context = kw['context']
    request = kw['request']

    #Add all selectable plugins to schema. This chooses the poll method to use
    method_choices = set()

    for (name, method) in request.registry.getAdapters([context], IElectoralRegisterMethod):
        method_choices.add((name, method.title))

    return deform.widget.SelectWidget(values=method_choices)

@colander.deferred
def register_diff_choices_widget(node, kw):
    context = kw['context']
    request = kw['request']
    api = kw['api']
    register = request.registry.getAdapter(context, IElectoralRegister)
    archive = register.archive

    choices = set()
    for id in sorted(archive.keys(), key=int, reverse=True):
        choices.add((id, api.dt_util.dt_format(archive[id]['time']), ))

    return deform.widget.SelectWidget(values=choices)


@schema_factory('AddEligibleVoter',
                title = _(u"add_eligible_voter_to_meeting",
                          default = u"Add an eligible voter to meeting"))
class AddEligibleVoterSchema(colander.Schema):
    userid = colander.SchemaNode(
        colander.String(),
        title = _(u"UserID"),
        description = _(u"single_permission_schema_userid_description",
                        default = u"Start typing the first letters of the UserID you want to add. You should see a popup below if that UserID exists."),
        validator=deferred_viewer_userid_validator,
        widget=deferred_autocompleting_viewer_userid_widget,
    )
    
    
@schema_factory('ElectoralRegisterHandler')
class ElectoralRegisterMethodSchema(colander.Schema):
    method = colander.SchemaNode(colander.String(),
                                  title = _(u"electoral_register_method", default=u"Method"),
                                  description = _(u"electoral_register_method_description",
                                                      default=u""),
                                  widget = electoral_register_method_choices_widget,
                                  )
    
    
@schema_factory('ElectoralRegisterDiff')
class ElectoralRegisterDiffSchema(colander.Schema):
    archive1 = colander.SchemaNode(colander.String(),
                                  title = _(u"electoral_register_diff_archive1", default=u"First register"),
                                  description = _(u"electoral_register_diff_archive1_description",
                                                    default=u""),
                                  widget = register_diff_choices_widget,
                                  )
    archive2 = colander.SchemaNode(colander.String(),
                                  title = _(u"electoral_register_diff_archive2", default=u"Second register"),
                                  description = _(u"electoral_register_diff_archive2_description",
                                                    default=u""),
                                  widget = register_diff_choices_widget,
                                  )