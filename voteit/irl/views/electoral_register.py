import deform
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
from pyramid.decorator import reify
from betahaus.viewcomponent import view_action
from voteit.core.models.interfaces import IMeeting
from arche.views.base import BaseView
from voteit.core.security import MODERATE_MEETING

from voteit.irl import _
from voteit.irl.models.interfaces import IElectoralRegister
from voteit.irl.schemas import ElectoralRegisterDiffSchema
from arche.events import SchemaCreatedEvent
from zope.component.event import objectEventNotify


@view_defaults(context = IMeeting, permission = MODERATE_MEETING)
class ElectoralRegisterView(BaseView):
    """ Handle electoral register. Note that all view methods for this must use the
        meeting as a context, otherwise some things might not work. (Like the adapter)
    """

    @reify
    def electoral_register(self):
        return self.request.registry.getAdapter(self.context, IElectoralRegister)

    def _registers_reverse(self):
        registers = [(k, v) for (k, v) in self.electoral_register.registers.items()]
        registers.reverse()
        return registers

    def _view_reg_link(self, id):
        return self.request.resource_url(self.context, 'view_electoral_register', query={'id': id})

    @view_config(name = "electoral_register",
                 renderer = "voteit.irl:templates/electoral_register.pt")
    def electoral_register_view(self):
        if self.request.GET.get('update_register', False):
            userids = self.electoral_register.currently_set_voters()
            self.electoral_register.new_register(userids)
            msg = _(u"New electoral register added")
            self.flash_messages.add(msg)
            url = self.request.resource_url(self.context, 'electoral_register')
            return HTTPFound(location = url)
        self.response['current_reg'] = self.electoral_register.current
        self.response['new_reg_needed'] = self.electoral_register.new_register_needed()
        self.response['electoral_register'] = self.electoral_register
        self.response['registers_list'] = self._registers_reverse()
        self.response['view_reg_link'] = self._view_reg_link
        return self.response

    @view_config(name = "view_electoral_register",
                 renderer = "voteit.irl:templates/view_electoral_register.pt")
    def view_electoral_register(self):
        id = int(self.request.GET.get('id'))
        self.response['id'] = id
        self.response['register'] = self.electoral_register.registers[id]
        return self.response

    @view_config(name = "diff_electoral_register",
                 renderer = "voteit.irl:templates/diff_electoral_register.pt")
    def diff_electoral_register_view(self):
        post = self.request.POST
        if 'back' in post:
            url = self.request.resource_url(self.context, 'electoral_register')
            return HTTPFound(location = url)
        
        schema = ElectoralRegisterDiffSchema()
        objectEventNotify(SchemaCreatedEvent(schema))
        schema = schema.bind(context = self.context, request = self.request, view = self)
        form = deform.Form(schema, buttons=(deform.Button('diff', _(u"Diff"), css_class="btn btn-primary"),
                                            deform.Button('back', _(u"Back"), css_class="btn btn-default"),))
        if 'diff' in post:
            controls = post.items()
            try:
                appstruct = form.validate(controls)
                self.response['form'] = form.render(appstruct = appstruct)
                self.append_diff_info(appstruct['first'], appstruct['second'])
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
        else:
            self.response['form'] = form.render()
        return self.response

    def append_diff_info(self, first, second):
        first_reg_users = self.electoral_register.registers[first]['userids']
        second_reg_users = self.electoral_register.registers[second]['userids']
        self.response.update({'show_diff': True,
                              'first': first,
                              'second': second,
                              'added_userids': first_reg_users - second_reg_users,
                              'removed_userids': second_reg_users - first_reg_users})


@view_action('participants_menu', 'electoral_register',
             title = _(u"Electoral register"),
             link = "electoral_register",
             permission = MODERATE_MEETING)
def electoral_register_moderator_menu_link(context, request, va, **kw):
    url = request.resource_url(request.meeting, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, request.localizer.translate(va.title))
