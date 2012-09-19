from deform import Form
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import find_root
from betahaus.viewcomponent import view_action
from voteit.core.models.interfaces import IMeeting
from voteit.core.views.base_view import BaseView
from voteit.core.security import VIEW
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import ROLE_VOTER
from voteit.core.security import ROLE_VIEWER
from voteit.core.security import context_effective_principals
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_add
from voteit.core.models.schemas import button_cancel
from deform.exception import ValidationFailure


from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.fanstaticlib import voteit_irl
from voteit.irl.models.interfaces import IEligibleVoters
from voteit.irl.schemas import AddEligibleVoterSchema

class EligibleVotersView(BaseView):
    
    def __init__(self, context, request):
        super(EligibleVotersView, self).__init__(context, request)
        self.eligible_voters = self.request.registry.getAdapter(self.context, IEligibleVoters)
        voteit_irl.need()

    @view_config(name="view_eligible_voters", context=IMeeting, renderer="templates/eligible_voters.pt", permission=MODERATE_MEETING)
    def view(self):
        root = self.api.root
        
        def _get_user(userid):
            return root['users'][userid]
        
        self.response['get_user'] = _get_user
        self.response['eligible_voters'] = self.eligible_voters.list
        
        return self.response
    
    @view_config(name="add_eligible_voter", context=IMeeting, renderer="voteit.core.views:templates/base_edit.pt", permission=MODERATE_MEETING)
    def add(self):
        schema = AddEligibleVoterSchema().bind(context=self.context, request=self.request, api=self.api)
        add_csrf_token(self.context, self.request, schema)
        
        form = Form(schema, buttons=(button_add, button_cancel))
        self.api.register_form_resources(form)

        post = self.request.POST
        if 'add' in post:
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
        
            self.eligible_voters.list.add(appstruct['userid'])        
            self.api.flash_messages.add(_(u"Successfully added"))
        
            return HTTPFound(location=self.request.resource_url(self.context, 'view_eligible_voters'))
        
        if 'cancel' in post:
            self.api.flash_messages.add(_(u"Canceled"))

            return HTTPFound(location=self.request.resource_url(self.context, 'view_eligible_voters'))
        
        self.response['form'] = form.render()
        return self.response
    
    @view_config(name="remove_eligible_voter", context=IMeeting, permission=MODERATE_MEETING)
    def remove(self):
        if 'userid' in self.request.GET:
            userid = self.request.GET.get('userid', '')
            self.eligible_voters.list.remove(userid)
        
        return HTTPFound(location=self.request.resource_url(self.context, 'view_eligible_voters'))