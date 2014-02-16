import colander
import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from betahaus.viewcomponent.decorators import view_action
from betahaus.pyracont.factories import createSchema
from voteit.core.views.base_edit import BaseEdit
from voteit.core import VoteITMF as vmf
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import ROLE_OWNER
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.models.schemas import button_update
from voteit.core.models.schemas import button_cancel

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.schemas import add_proposals_owner_nodes


class ChangeProposalsOwner(BaseEdit):

    @view_config(name="proposals_owner", context = IAgendaItem, permission = MODERATE_MEETING,
                 renderer = 'voteit.core:views/templates/base_edit.pt')
    def change_proposal_owners(self):
        """ Change proposal owners. """
        proposals = self.context.get_content(iface = IProposal, sort_on = 'created')
        schema = colander.Schema()
        add_proposals_owner_nodes(schema, proposals)
        schema = schema.bind(context = self.context, request = self.request, api = self.api)
        back_url = self.request.resource_url(self.context)
        if not proposals:
            self.api.flash_messages.add(_(u"No proposals here"))
            return HTTPFound(location = back_url)
        form = deform.Form(schema, buttons = (button_update, button_cancel,))
        self.api.register_form_resources(form)
        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(vmf(u"Canceled"))
            return HTTPFound(location = url)
        if 'update' in self.request.POST:
            controls = self.request.POST.items()
            try:
                #appstruct is deforms convention. It will be the submitted data in a dict.
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            updated = set()
            for (prop_name, owner) in appstruct.items():
                proposal = self.context[prop_name]
                old_owner = proposal.creators[0]
                if owner == old_owner:
                    continue
                #Remove Owner group from old owner?
                groups = list(proposal.get_groups(old_owner))
                if ROLE_OWNER in groups:
                    groups.remove(ROLE_OWNER)
                    proposal.set_groups(old_owner, groups)
                #Add group owner to new owner
                proposal.add_groups(owner, [ROLE_OWNER])
                #Set new owner in creators attr - this will also trigger reindex catalog event so keep it last!
                proposal.set_field_appstruct({'creators': (owner,)})
                updated.add(prop_name)
            if updated:
                self.api.flash_messages.add(vmf(u"Successfully updated"))
            else:
                self.api.flash_messages.add(vmf(u"Nothing updated"))
            return HTTPFound(location = back_url)
        appstruct = dict([(prop.__name__, prop.creators[0]) for prop in proposals])
        self.response['form'] = form.render(appstruct = appstruct)
        return self.response


@view_action('context_actions', 'change_owner', title = _(u"Change proposals owner"),
             permission = MODERATE_MEETING, interface = IAgendaItem)
def change_owner_menu_action(context, request, va, **kw):
    api = kw['api']
    url = request.resource_url(context, 'proposals_owner')
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))
