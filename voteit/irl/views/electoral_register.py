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


class ElectoralRegisterView(BaseView):
    """ Handle electoral register
    """
    
    def __init__(self, context, request):
        super(ElectoralRegisterView, self).__init__(context, request)
        self.register = self.request.registry.getAdapter(self.context, IElectoralRegister)
        voteit_irl.need()

    @view_config(name="clear_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def clear(self):
        """ Remove vote permissions and clear registry
        """
        self.register.clear()
        
        self.api.flash_messages.add(_(u"Electoral register is cleared."))
        return HTTPFound(location=resource_url(self.context, self.request))
        
    @view_config(name="add_electoral_register", context=IMeeting, permission=VIEW)
    def add(self):
        """ Set someone as attending
        """
        userid = authenticated_userid(self.request)
        self.register.add(userid)
        
        self.api.flash_messages.add(_(u"Thanks, you have registered your attendance."))
        return HTTPFound(location=resource_url(self.context, self.request))
        
    @view_config(name="close_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def close(self):
        """ Close registry
        """
        self.api.flash_messages.add(_(u"Closed"))
        self.register.close()
        return HTTPFound(location=resource_url(self.context, self.request, 'view_electoral_register'))

    @view_config(name="view_electoral_register", context=IMeeting, renderer="templates/electoral_register.pt", permission=VIEW)
    def view(self):
        root = self.api.root
        
        def _get_user(userid):
            return root['users'][userid]
            
        voters = 0
        delegates = []
        reserves = []
        
        for userid in root.users.keys():
            try:
                id = int(userid)
                groups = self.context.get_groups(userid)
                if ROLE_VOTER in groups:
                    voters += 1
                if 101 <= id and id <= 201:
                    if ROLE_VOTER not in groups:
                        delegates.append(userid)
                if id >= 202:
                    if ROLE_VOTER in groups:
                        reserves.append(userid)
            except Exception:
                pass
        
        # total number of users with voting rights
        self.response['voters'] = voters
        # delegates without voting rights
        self.response['delegates'] = delegates
        # reserves with voting right
        self.response['reserves'] = reserves
        
        self.response['get_user'] = _get_user
        
        return self.response


@view_action('moderator_menu', 'clear_electoral_register', title = _(u"Clear electoral register"),
             link = "clear_electoral_register")
@view_action('moderator_menu', 'close_electoral_register', title = _(u"Close electoral register"),
             link = "close_electoral_register")
@view_action('moderator_menu', 'view_electoral_register', title = _(u"View electoral register"),
             link = "view_electoral_register")
def electoral_register_moderator_menu_link(context, request, va, **kw):
    api = kw['api']
    if not api.context_has_permission(MODERATE_MEETING, api.meeting):
        return ""
    url = request.resource_url(api.meeting, va.kwargs['link']) 
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))

@view_action('meeting_actions', 'add_electoral_register', title = _(u"Set yourself as present"))
def electoral_register_link(context, request, va, **kw):
    api = kw['api']
    if not api.userid or not api.meeting:
        return ''
    register = request.registry.getAdapter(api.meeting, IElectoralRegister)
    if register.register_closed:
        return ''
    try:
        int(api.userid)
    except ValueError:
        return ''
    if api.userid in register.register:
        return ''
    link = request.resource_url(api.meeting, 'add_electoral_register')
    return """ <li class="tab"><a href="%s">%s</a></li>"""  % (link, api.translate(va.title))
