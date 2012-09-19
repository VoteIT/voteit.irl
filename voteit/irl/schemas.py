import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from voteit.core.models.interfaces import IMeeting
from pyramid.traversal import find_interface
from voteit.core.security import context_effective_principals
from voteit.core.security import ROLE_VIEWER
from voteit.core.security import VIEW
from voteit.core.security import find_authorized_userids

from voteit.irl import VoteIT_IRL_MF as _


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
    
    
