from arche.utils import get_content_factories
from arche.views.base import BaseView
from betahaus.viewcomponent.decorators import view_action
from pyramid.httpexceptions import HTTPForbidden
from pyramid.traversal import resource_path
from pyramid.view import view_config
from pyramid.view import view_defaults
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IProposal
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import VIEW

from voteit.irl.fanstaticlib import voteit_irl_projector
from voteit.irl import _


@view_defaults(context = IMeeting, permission = MODERATE_MEETING)
class ProjectorView(BaseView):

    @view_config(name = '__projector__',
                 renderer = 'voteit.irl:templates/projector.pt',
                 permission = VIEW)
    def main_view(self):
        voteit_irl_projector.need()
        response = {}
        response['selected'] = selected = self.request.subpath and self.request.subpath[0] or None
        response['agenda_items'] = self.get_ais()
        response['state_titles'] = self.request.get_wf_state_titles(IAgendaItem, 'AgendaItem')
        return response

    @view_config(name = '__quick_poll__.json',
                 renderer = 'json')
    def quick_poll(self):
        proposals = []
        ai = None
        translate = self.request.localizer.translate
        for uid in self.request.POST.getall('uid'):
            prop = self.resolve_uid(uid = uid)
            proposals.append(prop)
            if ai is None:
                ai = prop.__parent__
            else:
                if ai != prop.__parent__:
                    raise HTTPForbidden("Proposals fetched from different agenda items")
        if not proposals:
            raise HTTPForbidden(translate(_("No proposals")))
        factories = get_content_factories()
        if len(proposals) == 1:
            reject_prop = factories['Proposal'](text = translate(_("Reject proposal")))
            ai[reject_prop.uid] = reject_prop
            proposals.append(reject_prop)
        title = _("Quick poll: ${proposals}",
                  mapping = {'proposals': ", ".join([x.aid for x in proposals])})
        title = translate(title)
        proposal_uids = [x.uid for x in proposals]
        if len(proposals) == 2:
            poll_plugin = 'majority_poll'
        else:
            #Kolla Schulze eller majoritet
            poll_plugin = 'schulze_stv'
        poll = factories['Poll'](title = title,
                                 proposals = proposal_uids,
                                 poll_plugin = poll_plugin)
        ai[poll.uid] = poll
        poll.set_workflow_state(self.request, 'upcoming')
        poll.set_workflow_state(self.request, 'ongoing')
        poll_url = '<a href="%s">%s</a>' % (self.request.resource_url(poll), title)
        return {'msg': translate(_("Added and started: ${poll_url}",
                                   {'poll_url': poll_url}))}

    @view_config(context = IAgendaItem, name = "__ai_contents__.json", renderer = 'json')
    def ai_contents(self):
        response = {}
        query = "path == '%s' and " % resource_path(self.context)
        query += "type_name == 'Proposal' and " #
        query += "workflow_state in any(['published', 'approved', 'denied'])"
        #sort_index = 'order'
        results = []
        for obj in self.catalog_query(query, resolve = True):
            results.append(dict(text = self.request.transform_text(obj.text),
                                aid = obj.aid,
                                prop_wf_url = self.request.resource_url(obj, '__change_state_projector__.json'),
                                wf_state = obj.get_workflow_state(),
                                uid = obj.uid,
                                creator = self.request.creators_info(obj.creator, portrait = False)))
        return {'agenda_item': self.context.title,
                'ai_url': self.request.resource_url(self.request.meeting, '__projector__', anchor = self.context.__name__),
                'proposals': results}

    def get_ais(self):
        results = {}
        states = ('ongoing', 'upcoming')
        query = "path == '%s' and " % resource_path(self.request.meeting)
        query += "type_name == 'AgendaItem' and "
        #query += "order > %s and " % ai.get_field_value('order')
        for state in states:
            results[state] = tuple(self.catalog_query("%s workflow_state == '%s'" % (query, state), resolve = True, sort_index = 'order'))
        return results

    @view_config(context = IProposal, name = "__change_state_projector__.json", renderer = 'json')
    def change_state_projector(self):
        """ Change workflow state for context.
            Returns result in json. Only state changes between 'published', 'approved' and 'denied'
            are allowed.
        """
        allowed_states = ('published', 'approved', 'denied')
        transl = self.request.localizer.translate
        if self.context.get_workflow_state() not in allowed_states:
            msg = _("wrong_initial_state_error",
                    default = "Proposal wasn't in any of the states "
                    "'Published', 'Approved' or 'Denied'. "
                    "You may need to reload this page.")
            return {'status': 'error',
                    'type': 'wrong_initial_state',
                    'msg': transl(msg)}
        state = self.request.POST.get('state')
        if state not in allowed_states:
            return {'status': 'error',
                    'type': 'wrong_new_state',
                    'msg': transl(_("Not allowed to transition to ${state}",
                                    mapping = {'state': state}))}
        self.context.set_workflow_state(self.request, state)
        return {'status': 'success',
                'state': state}

#     def get_next_name(self, ai):
#         query = "path == '%s' and " % resource_path(self.request.meeting)
#         query += "type_name == 'AgendaItem' and "
#         query += "workflow_state == '%s' and " % ai.get_workflow_state()
#         query += "order > %s" % ai.get_field_value('order')
#         for ai in self.catalog_query(query, resolve = True, sort_index = 'order', limit = 1):
#             return ai


@view_action('meeting_menu', 'projector',
             title = _(u"Proposal view for projector"),
             permission = MODERATE_MEETING)
def projector_menu_link(context, request, va, **kw):
    """ Visible in the moderator menu, but doesn't work for the meeting root """
    if IAgendaItem.providedBy(context):
        url = request.resource_url(request.meeting, '__projector__', anchor = context.__name__)
    else:
        url = request.resource_url(request.meeting, '__projector__')
    return """<li><a href="%s"> %s </a></li>""" % (url, request.localizer.translate(va.title))
