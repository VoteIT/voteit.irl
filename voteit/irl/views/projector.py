import re
from urllib import urlencode

from betahaus.viewcomponent.decorators import view_action
from pyramid.httpexceptions import HTTPForbidden
from pyramid.settings import truthy
from pyramid.traversal import resource_path
from pyramid.view import view_config
from pyramid.view import view_defaults
from repoze.catalog.query import Eq
from repoze.workflow import get_workflow

from voteit.core.helpers import TAG_PATTERN
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IProposal
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import VIEW
from voteit.core.views.agenda_item import AgendaItemView
from voteit.core import _ as core_ts

from voteit.irl import _
from voteit.irl.fanstaticlib import voteit_irl_projector

DEFAULT_CHECKED_WORKFLOW_STATES = ('published', 'approved', 'denied')


def proj_tags2links(text):
    """ Transform #tag to a relative link in this context.
        Not domain name or path will be included - it starts with './'
    """

    def handle_match(matchobj):
        matched_dict = matchobj.groupdict()
        tag = matched_dict['tag']
        pre = matched_dict['pre']
        url = u"?%s" % urlencode({'tag': tag.encode('utf-8')})
        # This should be refactored and handled through javascript
        return u"""%(pre)s<a href="#" data-tag-filter="%(tag)s">#%(tag)s</a>""" % \
               {'pre': pre, 'url': url, 'tag': tag}

    return re.sub(TAG_PATTERN, handle_match, text)


@view_defaults(context=IMeeting, permission=MODERATE_MEETING)
class ProjectorView(AgendaItemView):
    @view_config(name='__projector__',
                 renderer='voteit.irl:templates/projector.pt',
                 permission=VIEW)
    def main_view(self):
        voteit_irl_projector.need()
        response = {}
        response['agenda_items'] = self.get_ais()
        response['state_titles'] = self.request.get_wf_state_titles(IAgendaItem, 'AgendaItem')
        return response

    @view_config(name='__quick_poll__.json',
                 renderer='json')
    def quick_poll(self):
        proposals = []
        ai = None
        translate = self.request.localizer.translate
        factories = self.request.content_factories

        # Poll method
        poll_method = self.request.POST.get('quick-poll-method', None)
        reject_prop = self.request.POST.get('reject-prop', None)
        reject_prop = reject_prop in truthy

        for uid in self.request.POST.getall('uid'):
            prop = self.resolve_uid(uid=uid)
            proposals.append(prop)
            if ai is None:
                ai = prop.__parent__
            else:
                if ai != prop.__parent__:
                    raise HTTPForbidden("Proposals fetched from different agenda items")
        if reject_prop:
            if ai:  # Should be set, otherwise next step will die anyway
                prop = factories['Proposal'](
                    text=translate(_("Reject"))
                )
                ai[prop.uid] = prop
                proposals.append(prop)
        if not proposals:
            raise HTTPForbidden(translate(_("No proposals")))
        if len(proposals) != 2 and poll_method == 'majority':
            raise HTTPForbidden(
                translate(_("Majority polls must have exactly 2 proposals in them.")))
        if len(proposals) < 3 and poll_method == 'schulze':
            raise HTTPForbidden(translate(_("Use majority polls for 2 proposals.")))
        # Check if there are other ongoing polls
        query = Eq('type_name', 'Poll') & Eq('path', resource_path(ai)) & Eq('workflow_state',
                                                                             'ongoing')
        res = self.request.root.catalog.query(query)[0]
        if res.total:
            raise HTTPForbidden(
                _("quickpoll_ongoing_polls_error",
                  default="There are ongoing polls in this agenda item,"
                          "close them first."))
        title = self.get_quick_poll_title()
        proposal_uids = [x.uid for x in proposals]
        if poll_method == 'schulze':
            poll_plugin = 'schulze'
        if poll_method == 'majority':
            poll_plugin = 'majority_poll'
        poll = factories['Poll'](
            title=title,
            proposals=proposal_uids,
            poll_plugin=poll_plugin
        )
        ai[poll.uid] = poll
        poll.set_workflow_state(self.request, 'upcoming')
        poll.set_workflow_state(self.request, 'ongoing')
        poll_url = '<a href="%s">%s</a>' % (self.request.resource_url(poll), title)
        return {'msg': translate(_("Added and started: ${poll_url}",
                                   {'poll_url': poll_url}))}

    @view_config(context=IAgendaItem, name="__ai_contents__.json", renderer='json')
    def ai_contents(self):
        query = Eq('path', resource_path(self.context))
        query &= Eq('type_name', 'Proposal')
        # query += "workflow_state in any(['published', 'approved', 'denied'])"
        results = []
        for obj in self.catalog_query(query, resolve=True):
            results.append(
                dict(
                    text=self.request.render_proposal_text(obj, tag_func=proj_tags2links),
                    aid=obj.aid,
                    prop_wf_url=self.request.resource_url(obj, '__change_state_projector__.json'),
                    wf_state=obj.get_workflow_state(),
                    uid=obj.uid,
                    creator=self.request.creators_info(obj.creator, portrait=False, no_tag=True),
                    tags=obj.tags,
                )
            )
        next_obj = self.next_ai()
        next_url = ''
        next_title = getattr(next_obj, 'title', '')
        if next_obj:
            next_url = self.request.resource_url(next_obj, '__ai_contents__.json')
        previous_obj = self.previous_ai()
        previous_url = ''
        previous_title = getattr(previous_obj, 'title', '')

        active_workflow_states = [r['wf_state'] for r in results]
        wf = get_workflow(IProposal, 'Proposal')
        workflow_states = []
        for info in wf._state_info(IProposal):  # Public API goes through permission checker
            if info['name'] in active_workflow_states:
                workflow_states.append({
                    'name': info['name'],
                    'title': self.request.localizer.translate(core_ts(info['title'])),
                    'checked': info['name'] in DEFAULT_CHECKED_WORKFLOW_STATES,
                })

        if previous_obj:
            previous_url = self.request.resource_url(previous_obj, '__ai_contents__.json')
        return {'agenda_item': self.context.title,
                'ai_url': self.request.resource_url(self.request.meeting, '__projector__',
                                                    anchor=self.context.__name__),
                'ai_regular_url': self.request.resource_url(self.context),
                'proposals': results,
                'workflow_states': workflow_states,
                'next_url': next_url,
                'previous_url': previous_url,
                'next_title': next_title,
                'previous_title': previous_title}

    def get_ais(self):
        results = {}
        states = ('ongoing', 'upcoming')
        query = "path == '%s' and " % resource_path(self.request.meeting)
        query += "type_name == 'AgendaItem' and "
        ai_order = self.request.meeting.order

        def _sorter(ai):
            try:
                return ai_order.index(ai.__name__)
            except (ValueError, KeyError):
                return len(ai_order)

        for state in states:
            squery = "%s workflow_state == '%s'" % (query, state)
            results[state] = sorted(self.catalog_query(squery, resolve=True), key=_sorter)
        return results

    @view_config(context=IProposal, name="__change_state_projector__.json", renderer='json')
    def change_state_projector(self):
        """ Change workflow state for context.
            Returns result in json. Only state changes between 'published', 'approved' and 'denied'
            are allowed.
        """
        allowed_states = ('published', 'approved', 'denied')
        transl = self.request.localizer.translate
        if self.context.get_workflow_state() not in allowed_states:
            msg = _("wrong_initial_state_error",
                    default="Proposal wasn't in any of the states "
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
                                    mapping={'state': state}))}
        self.context.set_workflow_state(self.request, state)
        return {'status': 'success',
                'state': state}

    def get_quick_poll_title(self):
        query = Eq('path', resource_path(self.request.meeting)) & Eq('type_name', 'Poll')
        res = self.request.root.catalog.query(query)[0]
        title = _("Descision ${num}", mapping={'num': res.total + 1})
        return self.request.localizer.translate(title)


@view_action('agenda_actions', 'projector',
             title=_("Projector"),
             permission=MODERATE_MEETING)
def projector_menu_link(context, request, va, **kw):
    """ Visible in the moderator menu, but doesn't work for the meeting root """
    if IAgendaItem.providedBy(context):
        url = request.resource_url(request.meeting, '__projector__', anchor=context.__name__)
    else:
        url = request.resource_url(request.meeting, '__projector__')
    return """<li><a href="{url}" title="{title}">{title}</a></li>""".format(
        title=request.localizer.translate(va.title),
        url=url,
    )


def includeme(config):
    config.scan(__name__)
