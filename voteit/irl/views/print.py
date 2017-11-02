import colander
import deform
from arche.views.base import BaseForm
from arche.views.base import BaseView
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from voteit.core import security
from voteit.core.helpers import strip_and_truncate
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IDiscussionPost
from voteit.core.models.interfaces import IProposal
from webhelpers.html.converters import nl2br

from voteit.irl import _
from voteit.irl.fanstaticlib import voteit_irl_print_css


@view_config(name = "_print_proposals_form",
             context = IAgendaItem,
             permission = security.MODERATE_MEETING,
             renderer = "arche:templates/form.pt")
class PrintProposalsForm(BaseForm):

    @property
    def buttons(self):
        return (deform.Button('print', title = _("Print"), css_class = 'btn btn-primary'),
                self.button_cancel)

    def get_schema(self):
        schema = colander.Schema(title = _(u"Select proposals to print"),
                                 description = _(u"print_proposals_description",
                                                 default = u"Each proposal will be on its own page"))

        for prop in self.context.get_content(content_type = 'Proposal'):
            schema.add(colander.SchemaNode(colander.Bool(),
                                           name = prop.__name__,
                                           title = prop.get_field_value('aid'),
                                           description = prop.title))
        return schema

    def print_success(self, appstruct):
        self.request.session['print_proposal_ids'] = [name for (name, val) in appstruct.items() if val == True]
        return HTTPFound(location = self.request.resource_url(self.context, '_print_proposals'))


@view_config(name = "_print_discussions_form",
             context = IAgendaItem,
             permission = security.MODERATE_MEETING,
             renderer = "arche:templates/form.pt")
class PrintDiscussionsForm(BaseForm):

    @property
    def buttons(self):
        return (deform.Button('print', title = _("Print"), css_class = 'btn btn-primary'),
                self.button_cancel)

    def get_schema(self):
        schema = colander.Schema(title = _(u"Select discussion posts to print"),
                                 description = _(u"print_discussion_description",
                                                 default = u"Each post will be on its own page"))
        for post in self.context.get_content(content_type = 'DiscussionPost'):
            schema.add(colander.SchemaNode(colander.Bool(),
                                           name = post.__name__,
                                           title = strip_and_truncate(post.text, symbol = '[...]'),))
        return schema

    def print_success(self, appstruct):
        self.request.session['print_post_ids'] = [name for (name, val) in appstruct.items() if val == True]
        return HTTPFound(location = self.request.resource_url(self.context, '_print_discussions'))


@view_config(name = "_print_proposals",
             context = IAgendaItem,
             permission = security.VIEW,
             renderer = "voteit.irl:templates/print_proposals.pt")
class PrintProposalsView(BaseView):

    def __call__(self):
        voteit_irl_print_css.need()
        response = {}
        one_proposal = self.request.GET.get('proposal_id', None)
        if one_proposal:
            proposal_ids = [one_proposal]
        else:
            proposal_ids = self.request.session.pop('print_proposal_ids', ())
        dt_handler = self.request.dt_handler
        response['proposals'] = [self.context[x] for x in proposal_ids]
        response['now'] = dt_handler.format_dt(dt_handler.utcnow())
        response['nl2br'] = nl2br
        return response


@view_config(name = "_print_discussions",
             context = IAgendaItem,
             permission = security.VIEW,
             renderer = "voteit.irl:templates/print_discussions.pt")
class PrintDiscussionsView(BaseView):

    def __call__(self):
        voteit_irl_print_css.need()
        response = {}
        one_post = self.request.GET.get('post_id', None)
        if one_post:
            print_post_ids = [one_post]
        else:
            print_post_ids = self.request.session.pop('print_post_ids', ())
        dt_handler = self.request.dt_handler
        response['discussion_posts'] = [self.context[x] for x in print_post_ids]
        response['now'] = dt_handler.format_dt(dt_handler.utcnow())
        response['nl2br'] = nl2br
        return response


@view_action('proposal_extras', 'print_proposals',
             title = _(u"Print proposals"),
             interface = IAgendaItem)
def print_proposals_action(context, request, va, **kw):
    url = request.resource_url(context, '_print_proposals_form')
    return """<li><a href="%s">%s</a></li>""" % (url,
                                                 request.localizer.translate(va.title))


@view_action('discussion_extras', 'print_discussions',
             title = _(u"Print discussions"),
             interface = IAgendaItem)
def print_discussions_action(context, request, va, **kw):
    url = request.resource_url(context, '_print_discussions_form')
    return """<li><a href="%s">%s</a></li>""" % (url,
                                                 request.localizer.translate(va.title))


#The silly &nbsp; is to cause the icon to have correct height. Only icons won't do.
_PRINT_BTN = """
<a class="btn btn-default btn-xs" href="%s" title="%s">
&nbsp;
<span class="text-primary glyphicon glyphicon-print"></span>
&nbsp;
</a>
"""

@view_action('metadata_listing', 'print_proposal',
             title = _("Print this proposal"),
             interface = IProposal)
def print_this_proposal_action(context, request, va, **kw):
    url = request.resource_url(request.agenda_item, '_print_proposals', query = {'proposal_id': context.__name__})
    return _PRINT_BTN % (url, request.localizer.translate(va.title))


@view_action('metadata_listing', 'print_post',
             title = _("Print this post"),
             interface = IDiscussionPost)
def print_this_post_action(context, request, va, **kw):
    url = request.resource_url(request.agenda_item, '_print_discussions', query = {'post_id': context.__name__})
    return _PRINT_BTN % (url, request.localizer.translate(va.title))


def includeme(config):
    config.scan(__name__)
