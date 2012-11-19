import deform
from deform import Form
from deform.exception import ValidationFailure
from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from pyramid.decorator import reify
from pyramid.response import Response
from pyramid.renderers import render
from zope.component import getAdapter
from betahaus.viewcomponent import view_action

from voteit.core.models.interfaces import IMeeting
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_update
from voteit.core.models.schemas import button_cancel
from voteit.core.views.base_view import BaseView
from voteit.core.security import VIEW
from voteit.core.security import MODERATE_MEETING

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElectoralRegister
from voteit.irl.models.interfaces import IEligibleVoters
from voteit.irl.models.interfaces import IElectoralRegisterMethod
from voteit.irl.schemas import ElectoralRegisterMethodSchema
from voteit.irl.schemas import ElectoralRegisterDiffSchema
from voteit.irl.fanstaticlib import voteit_irl_set_as_present


class ElectoralRegisterView(BaseView):
    """ Handle electoral register
    """

    @reify
    def register(self):
        return self.request.registry.getAdapter(self.context, IElectoralRegister)

    @reify
    def eligible_voters(self):
        return self.request.registry.getAdapter(self.context, IEligibleVoters)

    @view_config(name="clear_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def clear(self):
        """ Remove vote permissions and clear registry
        """
        self.register.clear()
        
        self.api.flash_messages.add(_(u"Electoral register is cleared."))
        return HTTPFound(location=resource_url(self.context, self.request, 'electoral_register'))
        
    @view_config(name="register_meeting_presence", context=IMeeting, permission=VIEW,
                 renderer = "templates/register_meeting_presence.pt")
    def register_meeting_presence(self):
        """ Controls for setting yourself as attending
        """
        voteit_irl_set_as_present.need()
        self.response['current'] = self.register_current_status()
        return self.response

    def register_current_status(self, msg = u""):
        self.response['register_closed'] = self.register.register_closed
        self.response['is_registered'] = self.api.userid in self.register.register
        self.response['msg'] = msg
        return render("templates/meeting_presence_status.pt", self.response, request = self.request)

    @view_config(name="_register_set_attending", context=IMeeting, permission=VIEW, xhr=True)
    def register_set_attending(self):
        self.register.add(self.api.userid)
        msg = _(u"Successfully updated.")
        return Response(self.register_current_status(msg))

    @view_config(name="close_electoral_register", context=IMeeting, permission=MODERATE_MEETING)
    def close(self):
        """ Close registry
        """
        self.api.flash_messages.add(_(u"Closed"))
        self.register.close()
        return HTTPFound(location=resource_url(self.context, self.request, 'electoral_register'))

    @view_config(name="electoral_register", context=IMeeting, renderer="templates/electoral_register.pt", permission=VIEW)
    def view(self):
        method_schema = ElectoralRegisterMethodSchema().bind(context=self.context, request=self.request, api=self.api)
        add_csrf_token(self.context, self.request, method_schema)

        method_form = Form(method_schema,
                           action=self.request.resource_url(self.context, 'apply_electoral_register_method'), 
                           buttons=(button_update,))
        self.api.register_form_resources(method_form)
        
        diff_schema = ElectoralRegisterDiffSchema().bind(context=self.context, request=self.request, api=self.api)
        add_csrf_token(self.context, self.request, diff_schema)

        diff_form = Form(diff_schema,
                         action=self.request.resource_url(self.context, 'diff_electoral_register'), 
                         buttons=(deform.Button('view', _(u"View")),))
        self.api.register_form_resources(diff_form)
        
        self.response['method_form'] = method_form.render()
        self.response['register'] = self.register
        self.response['archive'] = self.register.archive
        self.response['diff_form'] = diff_form.render()
        
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
    
    @view_config(name="diff_electoral_register", context=IMeeting, renderer="templates/diff_electoral_register.pt", permission=VIEW)
    def diff_electoral_register(self):
        schema = ElectoralRegisterDiffSchema().bind(context=self.context, request=self.request, api=self.api)
        add_csrf_token(self.context, self.request, schema)

        form = Form(schema,
                    action=self.request.resource_url(self.context), 
                    buttons=(deform.Button('view', _(u"View")),))
        self.api.register_form_resources(form)
        
        post = self.request.POST
        if 'view' in post:
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            
            archive1 = self.register.archive[appstruct['archive1']]
            archive2 = self.register.archive[appstruct['archive2']]
            
            def _get_user(userid):
                root = self.api.root
                return root['users'][userid]
        
            self.response['get_user'] = _get_user
            self.response['archive1'] = archive1
            self.response['archive2'] = archive2
            self.response['union'] = set(archive1['userids']) | set(archive2['userids'])
             
            self.response['form'] = form.render(controls)
            
            return self.response
        
        return HTTPFound(location=self.request.resource_url(self.context, 'electoral_register'))
    
    @view_config(name="apply_electoral_register_method", context=IMeeting, renderer="voteit.core.views:templates/base_edit.pt", permission=MODERATE_MEETING)
    def apply_method(self):
        schema = ElectoralRegisterMethodSchema().bind(context=self.context, request=self.request)
        add_csrf_token(self.context, self.request, schema)

        form = Form(schema, buttons=(button_update, button_cancel, ))
        self.api.register_form_resources(form)

        post = self.request.POST
        if 'update' in post:
            controls = post.items()
            try:
                #appstruct is deforms convention. It will be the submitted data in a dict.
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            
            if len(self.register.archive) > 0:
                list = self.register.archive["%s" % len(self.register.archive)]

                method = getAdapter(self.context, name=appstruct['method'], interface=IElectoralRegisterMethod)
                method.apply(list['userids'])

                self.api.flash_messages.add(_(u"Successfully updated"))
            else:
                self.api.flash_messages.add(_(u"No register to apply method on"))
            
            return HTTPFound(location=resource_url(self.context, self.request, 'electoral_register'))

        if 'cancel' in post:
            self.api.flash_messages.add(_(u"Canceled"))
            return HTTPFound(location=resource_url(self.context, self.request, 'electoral_register'))

        self.response['form'] = form.render()
        return self.response


@view_action('participants_menu', 'electoral_register', title = _(u"Electoral register"),
             link = "electoral_register", permission=MODERATE_MEETING)
def electoral_register_moderator_menu_link(context, request, va, **kw):
    api = kw['api']
    if not api.context_has_permission(MODERATE_MEETING, api.meeting):
        return ""
    url = request.resource_url(api.meeting, va.kwargs['link']) 
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))

@view_action('participants_menu', 'register_meeting_presence', title = _(u"Set yourself as present"))
def electoral_register_link(context, request, va, **kw):
    api = kw['api']
    if not api.userid or not api.meeting:
        return ''
    link = request.resource_url(api.meeting, 'register_meeting_presence')
    return """ <li class="tab"><a href="%s">%s</a></li>"""  % (link, api.translate(va.title))
