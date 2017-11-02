from __future__ import unicode_literals

from arche.views.base import DefaultEditForm
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from voteit.core.models.interfaces import IMeeting
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import ROLE_VOTER

from voteit.irl import _
from voteit.irl.models.interfaces import IElectoralRegister
from voteit.irl.models.interfaces import IElegibleVotersMethod


@view_config(name = "update_elegible_voters",
             context = IMeeting,
             renderer = "arche:templates/form.pt",
             permission = MODERATE_MEETING)
class EligibleVotersForm(DefaultEditForm):
    title = _("Elegible voters")
    schema_name = 'eligible_voters_method'
    title = _("Eligible Voters")

    def save_success(self, appstruct):
        self.adjust_voters(appstruct['method_name'])
        url = self.request.resource_url(self.context, 'electoral_register')
        return HTTPFound(location = url)

    def adjust_voters(self, method_name):
        method = self.request.registry.getAdapter(self.context, IElegibleVotersMethod, name = method_name)
        new_voters = method.get_voters(request = self.request)
        if not isinstance(new_voters, frozenset):
            new_voters = frozenset(new_voters)
        electoral_register = self.request.registry.getAdapter(self.context, IElectoralRegister)
        current_voters = electoral_register.currently_set_voters()
        if current_voters == new_voters:
            msg = _(u"no_update_of_perms_needed_notice",
                    default = u"Method '${method_title}' applied but it reports no change needed.",
                    mapping = {'method_title': self.request.localizer.translate(method.title)})
            self.flash_messages.add(msg)
            return
        removed_voters = current_voters - new_voters
        added_voters = new_voters - current_voters
        for userid in removed_voters:
            self.context.del_groups(userid, (ROLE_VOTER,))
        for userid in added_voters:
            self.context.add_groups(userid, (ROLE_VOTER,))
        msg = _("updated_voter_permissions_notice",
                default = "Method '${method_title}' added ${added_count} and removed ${removed_count}.",
                mapping = {'method_title': self.request.localizer.translate(method.title),
                           'added_count': len(added_voters),
                           'removed_count': len(removed_voters)})
        self.flash_messages.add(msg)


@view_action('control_panel_poll', 'update_elegible_voters',
             title = _("Update elegible voters"),
             permission = MODERATE_MEETING)
def meeting_presence_link(context, request, va, **kw):
    link = request.resource_url(request.meeting, 'update_elegible_voters')
    return """ <li><a href="%s">%s</a></li>"""  % (link, request.localizer.translate(va.title))


def includeme(config):
    config.scan(__name__)
