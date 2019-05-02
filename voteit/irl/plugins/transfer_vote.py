import colander
from arche.security import principal_has_permisson
from arche.views.base import DefaultEditForm
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import resource_path
from pyramid.view import view_config
from repoze.catalog.query import Eq
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.views.control_panel import control_panel_link

from voteit.irl import _
from voteit.irl.schemas import meeting_userids_widget


def _enabled(meeting):
    return getattr(meeting, 'vote_transfer_enabled', False)


@view_action('user_menu', 'transfer_vote',
             permission = security.VIEW,
             priority=30,
             title = _("Transfer vote"))
def transfer_vote_menu(context, request, va, **kw):
    if _enabled(request.meeting) and \
            security.ROLE_VOTER in request.meeting.local_roles.get(request.authenticated_userid, ()):
        url = request.resource_url(request.meeting, 'transfer_vote')
        return """<li><a href="%s">%s</a></li>""" % \
               (url, request.localizer.translate(va.title))


@colander.deferred
class ReceivingUserIDValidator(object):
    def __init__(self, node, kw):
        self.context = kw['context']
        self.request = kw['request']
        assert IMeeting.providedBy(
            self.context), "context must be a meeting object, got %r" % self.context

    def __call__(self, node, value):
        if not principal_has_permisson(self.request, value, security.VIEW, context=self.context):
            raise colander.Invalid(node, _("${userid} doesn't exist in this meeting.",
                                           mapping={'userid': value}))
        if security.ROLE_VOTER in self.context.get_groups(value):
            raise colander.Invalid(node, _("${userid} is already a voter.",
                                           mapping={'userid': value}))


class TransferVoteSchema(colander.Schema):
    to_userid = colander.SchemaNode(
        colander.String(),
        title=_("To userid"),
        description=_("Must be someone who isn't a voter right now."),
        validator=ReceivingUserIDValidator,
        widget=meeting_userids_widget,
    )


@view_config(context=IMeeting,
             name="transfer_vote",
             renderer="arche:templates/form.pt",
             permission=security.VIEW)
class TransferVoteForm(DefaultEditForm):
    schema_name = 'transfer_vote'
    title = _("Transfer vote")

    def __call__(self):
        if not _enabled(self.request.meeting):
            raise HTTPForbidden(_('Vote transfer is not currently enabled.'))
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
        userid = appstruct['to_userid']
        if userid is None:
            raise HTTPBadRequest("No userid found")
        self.context.del_groups(self.request.authenticated_userid, [security.ROLE_VOTER])
        self.context.add_groups(userid, [security.ROLE_VOTER])
        self.flash_messages.add(_("Vote transfered to ${userid}", mapping={'userid': userid}))
        return HTTPFound(location=self.request.resource_url(self.context))


class MeetingVoteTransferSettingsSchema(colander.Schema):
    vote_transfer_enabled = colander.SchemaNode(
        colander.Bool(),
        title=_("Enable users to transfer votes?"),
        description=_("Will add the option to the users profile menu."),
    )


@view_config(context=IMeeting,
             name="meeting_vote_transfer_settings",
             renderer="arche:templates/form.pt",
             permission=security.MODERATE_MEETING)
class MeetingPresenceSettingsForm(DefaultEditForm):
    type_name = 'Meeting'
    schema_name = 'vote_transfer_settings'
    title = _("Vote transfer settings")


def includeme(config):
    """ Include this to activate funcitonality to transfer vote to someone else."""
    # Set default value for attr
    from voteit.core.models.meeting import Meeting
    Meeting.vote_transfer_enabled = False
    # Include components
    config.scan(__name__)
    config.add_schema('Meeting', TransferVoteSchema, 'transfer_vote')
    config.add_schema('Meeting', MeetingVoteTransferSettingsSchema, 'vote_transfer_settings')
    config.add_view_action(
        control_panel_link,
        'control_panel_poll', 'vote_transfer_settings',
        title=_("Vote transfer setting"),
        view_name='meeting_vote_transfer_settings',
    )
