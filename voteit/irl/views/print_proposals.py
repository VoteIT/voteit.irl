import colander
import deform
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import find_interface
from pyramid.view import view_config
from arche.views.base import BaseForm, BaseView

from voteit.core import security
from voteit.core.models.interfaces import IAgendaItem, IProposal
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


@view_config(name = "_print_proposals",
             context = IAgendaItem,
             permission = security.MODERATE_MEETING,
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
        return response


@view_action('context_actions', 'print_proposals',
             title = _(u"Print proposals"),
             interface = IAgendaItem)
def print_proposals_action(context, request, va, **kw):
    url = request.resource_url(context, '_print_proposals_form')
    return """<li><a href="%s">%s</a></li>""" % (url,
                                                 request.localizer.translate(va.title))


@view_action('context_actions', 'print_proposal',
             title = _(u"Print this proposal"),
             interface = IProposal)
def print_this_proposal_action(context, request, va, **kw):
    ai = find_interface(context, IAgendaItem)
    url = request.resource_url(ai, '_print_proposals', query = {'proposal_id': context.uid})
    return """<li><a href="%s">%s</a></li>""" % (url,
                                                 request.localizer.translate(va.title))

def includeme(config):
    config.scan(__name__)
