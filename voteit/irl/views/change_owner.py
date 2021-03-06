import colander
from arche.views.base import DefaultEditForm
from betahaus.viewcomponent.decorators import view_action
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IDiscussionPost
from voteit.core.models.interfaces import IProposal
from voteit.core.security import MODERATE_MEETING

from voteit.irl import _
from voteit.irl.models.utils import change_ownership
from voteit.irl.schemas import add_discussions_owner_nodes
from voteit.irl.schemas import add_proposals_owner_nodes


class ChangeOwnershipBase(DefaultEditForm):

    def save_success(self, appstruct):
        updated = set()
        for (name, owner) in appstruct.items():
            obj = self.context[name]
            if change_ownership(obj, owner):
                updated.add(name)
        if updated:
            self.flash_messages.add(self.default_success)
        else:
            self.flash_messages.add(self.default_cancel)
        return HTTPFound(location = self.request.resource_url(self.context))


@view_config(name = "_proposal_owner",
             context = IAgendaItem,
             permission = MODERATE_MEETING,
             renderer = 'arche:templates/form.pt')
class ChangeOwnershipProposals(ChangeOwnershipBase):

    def appstruct(self):
        return dict([(x.__name__, x.creator[0]) for x in self.context.get_content(iface = IProposal, sort_on = 'created')])

    def get_schema(self):
        objects = self.context.get_content(iface = IProposal, sort_on = 'created')
        schema = colander.Schema()
        add_proposals_owner_nodes(schema, objects)
        return schema


@view_config(name = "_discussion_owner",
             context = IAgendaItem,
             permission = MODERATE_MEETING,
             renderer = 'arche:templates/form.pt')
class ChangeOwnershipDiscussionPosts(ChangeOwnershipBase):

    def appstruct(self):
        return dict([(x.__name__, x.creator[0]) for x in self.context.get_content(iface = IDiscussionPost, sort_on = 'created')])

    def get_schema(self):
        objects = self.context.get_content(iface = IDiscussionPost, sort_on = 'created')
        schema = colander.Schema()
        add_discussions_owner_nodes(schema, objects)
        return schema


@view_action('proposal_extras', 'change_proposal_owner',
             title = _(u"Change proposal ownership"),
             permission = MODERATE_MEETING,
             interface = IAgendaItem,
             link = '_proposal_owner')
@view_action('discussion_extras', 'change_discussion_owner',
             title = _(u"Change post ownership"),
             permission = MODERATE_MEETING,
             interface = IAgendaItem,
             link = '_discussion_owner')
def change_owner_menu_action(context, request, va, **kw):
    url = request.resource_url(context, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, request.localizer.translate(va.title))


def includeme(config):
    config.scan(__name__)
