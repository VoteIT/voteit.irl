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

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.fanstaticlib import voteit_irl
from voteit.irl.models.interfaces import IElectoralRegister
from voteit.irl.models.interfaces import IEligibleVoters


class ElectoralRegisterView(BaseView):
    """ Handle electoral register
    """
    
    def __init__(self, context, request):
        super(ElectoralRegisterView, self).__init__(context, request)
        self.register = self.request.registry.getAdapter(self.context, IElectoralRegister)
        self.eligible_voters = self.request.registry.getAdapter(self.context, IEligibleVoters)
        voteit_irl.need()

    @view_config(name="clear_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def clear(self):
        """ Remove vote permissions and clear registry
        """
        self.register.clear()
        
        self.api.flash_messages.add(_(u"Electoral register is cleared."))
        return HTTPFound(location=resource_url(self.context, self.request, 'electoral_register'))
        
    @view_config(name="add_electoral_register", context=IMeeting, permission=VIEW)
    def add(self):
        """ Set someone as attending
        """
        self.register.add(self.api.userid)
        
        self.api.flash_messages.add(_(u"Thanks, you have registered your attendance."))
        return HTTPFound(location=resource_url(self.context, self.request))
        
    @view_config(name="close_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def close(self):
        """ Close registry
        """
        self.api.flash_messages.add(_(u"Closed"))
        self.register.close()
        return HTTPFound(location=resource_url(self.context, self.request, 'electoral_register'))

    @view_config(name="electoral_register", context=IMeeting, renderer="templates/electoral_register.pt", permission=VIEW)
    def view(self):
        self.response['register'] = self.register
        self.response['archive'] = self.register.archive
        
        return self.response
    
    @view_config(name="view_electoral_register", context=IMeeting, renderer="templates/view_electoral_register.pt", permission=VIEW)
    def view_electoral_register(self):
        id = self.request.GET.get('id', None)
        try:
            if id in self.register.archive:
                root = self.api.root
                
                def _get_user(userid):
                    return root['users'][userid]
        
                self.response['get_user'] = _get_user
                self.response['time'] = self.register.archive[id]['time']
                self.response['userids'] = self.register.archive[id]['userids']
                
                return self.response
        
        except:
            pass
        
        self.api.flash_messages.add(_(u"No electoral register with that number"))
        return HTTPFound(location=resource_url(self.context, self.request, 'electoral_register'))


@view_action('participants_menu', 'electoral_register', title = _(u"Electoral register"),
             link = "electoral_register", permission=MODERATE_MEETING)
def electoral_register_moderator_menu_link(context, request, va, **kw):
    api = kw['api']
    if not api.context_has_permission(MODERATE_MEETING, api.meeting):
        return ""
    url = request.resource_url(api.meeting, va.kwargs['link']) 
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))

@view_action('participants_menu', 'add_electoral_register', title = _(u"Set yourself as present"))
def electoral_register_link(context, request, va, **kw):
    api = kw['api']
    if not api.userid or not api.meeting:
        return ''
    register = request.registry.getAdapter(api.meeting, IElectoralRegister)
    if register.register_closed:
        return ''
    if api.userid in register.register:
        return ''
    link = request.resource_url(api.meeting, 'add_electoral_register')
    return """ <li class="tab"><a href="%s">%s</a></li>"""  % (link, api.translate(va.title))