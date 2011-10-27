from pyramid.view import view_config

from voteit.core.views.base_view import BaseView
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.security import MODERATE_MEETING


class ProjectorView(BaseView):

    @view_config(context=IAgendaItem, name="projector", renderer="templates/projector.pt", permission=MODERATE_MEETING)
    def view(self):
        """ """

        self.response['proposals'] = self.api.get_restricted_content(self.context, iface=IProposal, sort_on='created', states=('published', 'approved', 'denied', ))
        
        return self.response
