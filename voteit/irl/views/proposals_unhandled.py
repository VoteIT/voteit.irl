import colander
from arche.security import PERM_MANAGE_SYSTEM
from arche.views.base import DefaultEditForm
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from voteit.core.models.interfaces import IMeeting

from voteit.irl import _


@view_config(name = "adjust_proposals_to_unhandled",
             context = IMeeting,
             permission = PERM_MANAGE_SYSTEM,
             renderer = "arche:templates/form.pt")
class ProposalsToUnhandledForm(DefaultEditForm):
    title = "Adjust all published proposals in ongoing AIs to unhandled?"

    def get_schema(self):
        return colander.Schema()

    def save_success(self, appstruct):
        count = 0
        for ai in self.context.get_content(content_type = 'AgendaItem', states = ['ongoing']):
            for proposal in ai.get_content(content_type = 'Proposal', states = ['published']):
                proposal.set_workflow_state(self.request, 'unhandled')
                count += 1
        self.flash_messages.add(_(u"Changed ${count} proposals",
                                  mapping = {'count': count}))
        return HTTPFound(location = self.request.resource_url(self.context))


@view_action('actions_menu', 'adjust_proposals_to_unhandled',
             title = "Proposals to unhandled",
             permission = PERM_MANAGE_SYSTEM,
             priority=10)
def adjust_proposals_to_unhandled(context, request, va, **kw):
    if request.meeting:
        url = request.resource_url(request.meeting, 'adjust_proposals_to_unhandled')
        return """<li><a href="%s">%s</a></li>""" % (url,
                                                     request.localizer.translate(va.title))

def includeme(config):
    config.scan(__name__)