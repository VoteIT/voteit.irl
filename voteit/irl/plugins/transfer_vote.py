from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import resource_path
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.schemas.common import deferred_autocompleting_userid_widget
from voteit.core.views.base_edit import BaseForm
import colander

from voteit.irl import _


@view_action('participants_menu', 'transfer_vote', title = _(u"Transfer vote"))
def generic_menu_link(context, request, va, **kw):
    """ This is for simple menu items for the meeting root """
    api = kw['api']
    if security.ROLE_VOTER in api.cached_effective_principals:
        url = request.resource_url(api.meeting, 'transfer_vote')
        return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))


@colander.deferred
def deferred_validate_receiving_userid(node, kw):
    context = kw['context']
    request = kw['request']
    return ReceivingUserIDValidator(context, request)


class ReceivingUserIDValidator(object):

    def __init__(self, context, request):
        assert IMeeting.providedBy(context), "context must be a meeting object, got %r" % context
        self.context = context
        self.request = request

    def __call__(self, node, value):
        if value not in security.find_authorized_userids(self.context, [security.VIEW]):
            raise colander.Invalid(node, _("${userid} doesn't exist in this meeting.",
                                           mapping = {'userid': value}))
        if security.ROLE_VOTER in self.context.get_groups(value):
            raise colander.Invalid(node, _("${userid} is already a voter.",
                                           mapping = {'userid': value}))


class TransferVoteSchema(colander.Schema):
    to_userid = colander.SchemaNode(colander.String(),
                                    title = _("To userid"),
                                    description = _("Must be someone who isn't a voter right now."),
                                    validator = deferred_validate_receiving_userid,
                                    widget = deferred_autocompleting_userid_widget)


class TransferVoteForm(BaseForm):

    def __call__(self):
        if security.ROLE_VOTER not in self.api.cached_effective_principals:
            raise HTTPForbidden(_("You're not a voter"))
        query = {'content_type': 'Poll',
                 'path': resource_path(self.context),
                 'workflow_state': 'ongoing'}
        res = self.api.search_catalog(**query)[0]
        if res.total > 0:
            raise HTTPForbidden(_("Votes can't be transfered while a poll is open."))
        return super(TransferVoteForm, self).__call__()

    def get_schema(self):
        return TransferVoteSchema()

    def save_success(self, appstruct):
        userid = appstruct.pop('to_userid')
        self.context.del_groups(self.request.authenticated_userid, [security.ROLE_VOTER])
        self.context.add_groups(userid, [security.ROLE_VOTER])
        self.api.flash_messages.add(_("Vote transfered to ${userid}", mapping = {'userid': userid}))
        return HTTPFound(location = self.api.meeting_url)


def includeme(config):
    """ Include this to activate funcitonality to transfer vote to someone else."""
    config.scan()
    config.add_view(TransferVoteForm,
                    context = IMeeting,
                    permission = security.VIEW,
                    name = 'transfer_vote',
                    renderer = "voteit.core:views/templates/base_edit.pt")
