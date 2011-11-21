from pyramid.view import view_config
from pyramid.renderers import render
from pyramid.renderers import render_to_response
from pyramid.traversal import resource_path
from pyramid.traversal import find_interface
from voteit.core.views.base_view import BaseView
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.security import MODERATE_MEETING
from betahaus.viewcomponent.decorators import view_action

from voteit.irl.fanstaticlib import voteit_irl
from voteit.irl import VoteIT_IRL_MF as _


class ProjectorView(BaseView):

    @view_config(context=IAgendaItem, name="projector", renderer="templates/projector.pt", permission=MODERATE_MEETING)
    def view(self):
        """ """
        voteit_irl.need()
        
        context_path = resource_path(self.api.meeting)
        query = dict(
            content_type = 'AgendaItem',
            workflow_state = 'ongoing',
            path = context_path,
        )
        self.response['ai_brains'] = self.api.get_metadata_for_query(**query)
        self.response['proposals'] = self.api.get_restricted_content(self.context, iface=IProposal, sort_on='created', states=('published', 'approved', 'denied', ))
        self.response['render_proposal'] = self.render_proposal
        
        return self.response
        
    def render_proposal(self, context, request):
        self.response['proposal'] = context        
        return render("templates/projector/proposal.pt", self.response, request=request)
        
    @view_config(context=IProposal, name="projector_state", renderer="templates/projector/proposal.pt", permission=MODERATE_MEETING)
    def state_change(self):
        """ Change workflow state for context.
            Note that if this view is called without the required permission,
            it will raise a WorkflowError exception. This view should
            never be linked to without doing the proper permission checks first.
            (Since the WorkflowError is not the same as Pyramids Forbidden exception,
            which will be handled by the application.)
        """
        state = self.request.params.get('state')
        if (state == 'approved' or state == 'denied') and self.context.get_workflow_state() != 'published':
            self.context.set_workflow_state(self.request, 'published')
        self.context.set_workflow_state(self.request, state)
        
        self.response['proposal'] = self.context
        return self.response
        
    @view_config(context=IMeeting, name="projector_agenda_items", permission=MODERATE_MEETING)
    def agenda_items(self):
    
        return render_to_response("templates/projector/agenda_items.pt", response, request=request)


@view_action('moderator_menu', 'projector', title = _(u"Projector view"), link = u"@@projector")
def projector_menu_link(context, request, va, **kw):
    """ Visible in the moderator menu """
    #FIXME: Doesn't work in meeting root
    api = kw['api']
    url = u"%s/%s" % (request.path_url, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))
