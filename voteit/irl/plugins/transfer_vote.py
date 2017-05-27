import colander
from arche.views.base import DefaultEditForm
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import resource_path
from repoze.catalog.query import Eq
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.schemas.common import deferred_autocompleting_userid_widget

from voteit.irl import _
from voteit.irl.models.interfaces import IParticipantNumbers


@view_action('participants_menu', 'transfer_vote', title=_("Transfer vote"))
def generic_menu_link(context, request, va, **kw):
    """ This is for simple menu items for the meeting root """
    if security.ROLE_VOTER in request.meeting.local_roles.get(request.authenticated_userid, ()):
        url = request.resource_url(request.meeting, 'transfer_vote')
        return """<li><a href="%s">%s</a></li>""" % (url, request.localizer.translate(va.title))


def _convert_to_userid(context, value):
    """ Maybe convert a string with participant number to userid? """
    try:
        value = int(value)
    except ValueError:
        # Should be a regular text string
        return value
    pn = IParticipantNumbers(context)
    return pn.number_to_userid.get(value, None)


@colander.deferred
class ReceivingUserIDValidator(object):
    def __init__(self, node, kw):
        self.context = kw['context']
        self.request = kw['request']
        assert IMeeting.providedBy(
            self.context), "context must be a meeting object, got %r" % self.context

    def __call__(self, node, value):
        value = _convert_to_userid(self.context, value)
        if not value:
            raise colander.Invalid(node, _("No user has that participant number"))
        if value not in security.find_authorized_userids(self.context, [security.VIEW]):
            raise colander.Invalid(node, _("${userid} doesn't exist in this meeting.",
                                           mapping={'userid': value}))
        if security.ROLE_VOTER in self.context.get_groups(value):
            raise colander.Invalid(node, _("${userid} is already a voter.",
                                           mapping={'userid': value}))


class TransferVoteSchema(colander.Schema):
    to_userid = colander.SchemaNode(
        colander.String(),
        title=_("To userid or participant number"),
        description=_("Must be someone who isn't a voter right now."),
        validator=ReceivingUserIDValidator,
        widget=deferred_autocompleting_userid_widget
    )


class TransferVoteForm(DefaultEditForm):
    schema_name = 'transfer_vote'
    title = _("Transfer vote")

    def __call__(self):
        if security.ROLE_VOTER not in self.context.local_roles.get(
                self.request.authenticated_userid, ()):
            raise HTTPForbidden(_("You're not a voter"))
        query = Eq('type_name', 'Poll') & Eq('path', resource_path(self.context)) & Eq(
            'workflow_state', 'ongoing')
        res = self.request.root.catalog.query(query)[0]
        if res.total > 0:
            raise HTTPForbidden(_("Votes can't be transfered while a poll is open."))
        return super(TransferVoteForm, self).__call__()

    def save_success(self, appstruct):
        userid = appstruct.pop('to_userid')
        userid = _convert_to_userid(self.context, userid)
        if userid is None:
            raise HTTPBadRequest("No userid found")
        self.context.del_groups(self.request.authenticated_userid, [security.ROLE_VOTER])
        self.context.add_groups(userid, [security.ROLE_VOTER])
        self.flash_messages.add(_("Vote transfered to ${userid}", mapping={'userid': userid}))
        return HTTPFound(location=self.request.resource_url(self.context))


def includeme(config):
    """ Include this to activate funcitonality to transfer vote to someone else."""
    config.scan(__name__)
    config.add_view(TransferVoteForm,
                    context=IMeeting,
                    permission=security.VIEW,
                    name='transfer_vote',
                    renderer="arche:templates/form.pt")
    config.add_schema('Meeting', TransferVoteSchema, 'transfer_vote')
