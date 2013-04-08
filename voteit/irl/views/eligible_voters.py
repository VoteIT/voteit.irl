import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from betahaus.viewcomponent import view_action
from betahaus.pyracont.factories import createSchema

from voteit.core.models.interfaces import IMeeting
from voteit.core.views.base_view import BaseView
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import ROLE_VOTER
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_update
from voteit.core.models.schemas import button_cancel

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElegibleVotersMethod
from voteit.irl.models.interfaces import IElectoralRegister


class ElegibleVoters(BaseView):
    
    @view_config(name="update_elegible_voters", context=IMeeting, renderer="voteit.core.views:templates/base_edit.pt",
                 permission=MODERATE_MEETING)
    def update_elegible_voters_view(self):
        """ Apply a method to adjust voters. """
        post = self.request.POST
        if 'cancel' in post:
            return HTTPFound(location = self.api.meeting_url)
        schema = createSchema('ElegibleVotersMethodSchema')       
        add_csrf_token(self.context, self.request, schema)
        schema = schema.bind(context=self.context, request=self.request, api=self.api) 
        form = deform.Form(schema, buttons=(button_update, button_cancel, ))
        self.api.register_form_resources(form)
        if 'update' in post:
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            self.adjust_voters(appstruct['method_name'])
            url = self.request.resource_url(self.context, 'electoral_register')
            return HTTPFound(location = url)
        self.response['form'] = form.render()
        return self.response

    def adjust_voters(self, method_name):
        method = self.request.registry.getAdapter(self.context, IElegibleVotersMethod, name = method_name)
        new_voters = method.get_voters(context = self.context, request = self.request, api = self.api)
        if not isinstance(new_voters, frozenset):
            new_voters = frozenset(new_voters)
        electoral_register = self.request.registry.getAdapter(self.context, IElectoralRegister)
        current_voters = electoral_register.currently_set_voters()
        if current_voters == new_voters:
            msg = _(u"no_update_of_perms_needed_notice",
                    default = u"Method '${method_title}' applied but it didn't need to change anything.",
                    mapping = {'method_title': self.api.translate(method.title)})
            self.api.flash_messages.add(msg)
            return
        removed_voters = current_voters - new_voters
        added_voters = new_voters - current_voters
        for userid in removed_voters:
            self.context.del_groups(userid, (ROLE_VOTER,))
        for userid in added_voters:
            self.context.add_groups(userid, (ROLE_VOTER,))
        msg = _(u"updated_voter_permissions_notice",
                default = u"Method '${method_title}' added ${added_count} and removed ${removed_count}.",
                mapping = {'method_title': self.api.translate(method.title),
                           'added_count': len(added_voters),
                           'removed_count': len(removed_voters)})
        self.api.flash_messages.add(msg)


@view_action('participants_menu', 'update_elegible_voters', title = _(u"Update elegible voters"), permission = MODERATE_MEETING)
def meeting_presence_link(context, request, va, **kw):
    api = kw['api']
    link = request.resource_url(api.meeting, 'update_elegible_voters')
    return """ <li class="tab"><a href="%s">%s</a></li>"""  % (link, api.translate(va.title))
