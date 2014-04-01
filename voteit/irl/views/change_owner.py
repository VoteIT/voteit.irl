import colander
import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from betahaus.viewcomponent.decorators import view_action
from betahaus.pyracont.factories import createSchema
from voteit.core.views.base_edit import BaseEdit
from voteit.core import VoteITMF as vmf
from voteit.core.security import MODERATE_MEETING
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IDiscussionPost
from voteit.core.models.interfaces import IProposal
from voteit.core.models.schemas import button_update
from voteit.core.models.schemas import button_cancel

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.utils import change_ownership
from voteit.irl.schemas import (add_proposals_owner_nodes,
                                add_discussions_owner_nodes)


class ChangeOwnership(BaseEdit):

    def change_ownership(self, objects, schema):
        schema = schema.bind(context = self.context, request = self.request, api = self.api)
        back_url = self.request.resource_url(self.context)
        if not objects:
            self.api.flash_messages.add(_(u"No proposals here"))
            return HTTPFound(location = back_url)
        form = deform.Form(schema, buttons = (button_update, button_cancel,))
        self.api.register_form_resources(form)
        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(vmf(u"Canceled"))
            return HTTPFound(location = back_url)
        if 'update' in self.request.POST:
            controls = self.request.POST.items()
            try:
                #appstruct is deforms convention. It will be the submitted data in a dict.
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            updated = set()
            for (name, owner) in appstruct.items():
                obj = self.context[name]
                if change_ownership(obj, owner):
                    updated.add(name)
            if updated:
                self.api.flash_messages.add(vmf(u"Successfully updated"))
            else:
                self.api.flash_messages.add(vmf(u"Nothing updated"))
            return HTTPFound(location = back_url)
        appstruct = dict([(obj.__name__, obj.creators[0]) for obj in objects])
        self.response['form'] = form.render(appstruct = appstruct)
        return self.response

    @view_config(name="_proposal_owner", context = IAgendaItem, permission = MODERATE_MEETING,
                 renderer = 'voteit.core:views/templates/base_edit.pt')
    def proposal_ownership(self):
        objects = self.context.get_content(iface = IProposal, sort_on = 'created')
        schema = colander.Schema()
        add_proposals_owner_nodes(schema, objects)
        return self.change_ownership(objects, schema)

    @view_config(name="_discussion_owner", context = IAgendaItem, permission = MODERATE_MEETING,
                 renderer = 'voteit.core:views/templates/base_edit.pt')
    def discussion_ownership(self):
        objects = self.context.get_content(iface = IDiscussionPost, sort_on = 'created')
        schema = colander.Schema()
        add_discussions_owner_nodes(schema, objects)
        return self.change_ownership(objects, schema)


@view_action('context_actions', 'change_proposal_owner', title = _(u"Change proposal ownership"),
             permission = MODERATE_MEETING, interface = IAgendaItem, link = '_proposal_owner')
@view_action('context_actions', 'change_discussion_owner', title = _(u"Change discussion ownership"),
             permission = MODERATE_MEETING, interface = IAgendaItem, link = '_discussion_owner')
def change_owner_menu_action(context, request, va, **kw):
    api = kw['api']
    url = request.resource_url(context, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))
