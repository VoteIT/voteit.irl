import re
from urllib import urlencode

from betahaus.viewcomponent.decorators import view_action
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPNotFound
from pyramid.settings import truthy
from pyramid.traversal import resource_path
from pyramid.view import view_config
from pyramid.view import render_view_to_response
from pyramid.view import view_defaults
from repoze.catalog import query
from repoze.workflow import get_workflow
from voteit.core.helpers import TAG_PATTERN
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IDiffText
from voteit.core.models.interfaces import IPollPlugin
from voteit.core.models.interfaces import IPoll
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IProposal
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import VIEW
from voteit.core.views.agenda_item import AgendaItemView
from voteit.core import _ as core_ts, security

from voteit.irl import _
from voteit.irl.fanstaticlib import voteit_irl_projector


DEFAULT_CHECKED_WORKFLOW_STATES = ('published', 'voting')
QUICK_SELECT_WORKFLOW_STATES = ('published', 'approved', 'denied')

JS_TRANSLATIONS = [
    _("Previous"),
    _("Next"),
    _("by"),
    _("Click in menu to select Agenda Item"),
    _("Ongoing polls"),
    _("Closed polls"),
    _("Close poll"),
    _("Show last poll result"),
    _('add reject'),
    _('votes'),
    core_ts('Close'),
]

POLL_GROUPS = [
    {
        'title': _('Multiple winners (Schulze)'),
        'methods': [  # params: Poll name and whether to add deny proposal.
            ('schulze', False),
            ('schulze', True),
        ]
    }, {
        'title': _('Majority poll'),
        'methods': [
            ('majority_poll', False),
            ('combined_simple', False),
        ]
    }
]

POLL_INTERVAL_TIME = 3  # Time in seconds. Maybe should be a setting?


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
        return {}

    def serialize_ai(self, ai):
        return {
            'title': ai.title,
            'href': self.request.resource_path(ai),
            'workflowState': ai.get_workflow_state(),
            'uid': ai.uid,
            'jsonUrl': self.request.resource_path(ai, '__content__.json'),
            'name': ai.__name__,
        }

    def _get_ais(self, *states):
        ai_query = query.Eq('path', resource_path(self.request.meeting))
        ai_query &= query.Eq('type_name', 'AgendaItem')
        if states:
            ai_query &= query.Any('workflow_state', states)
        ai_order = self.request.meeting.order
        def _sorter(ai):
            try:
                return ai_order.index(ai.__name__)
            except (ValueError, KeyError):
                return len(ai_order)

        return sorted(self.catalog_query(ai_query, resolve=True, perm=None), key=_sorter)

    def _get_workflow_states(self):
        wf = get_workflow(IProposal, 'Proposal')
        workflow_states = []
        for info in wf._state_info(IProposal):  # Public API goes through permission checker
            name = info['name']
            workflow_states.append({
                'name': name,
                'title': self.request.localizer.translate(core_ts(info['title'])),
                'checked': name in DEFAULT_CHECKED_WORKFLOW_STATES,
                'quickSelect': name in QUICK_SELECT_WORKFLOW_STATES,  # Enables projector wf change
            })
        return workflow_states

    def get_translation_strings(self):
        # type: () -> dict
        ts = {}
        for t in JS_TRANSLATIONS:
            ts[t] = self.request.localizer.translate(t)
        ts.update(self.request.get_wf_state_titles(IAgendaItem, 'AgendaItem'))
        ts.update(self.request.get_wf_state_titles(IPoll, 'Poll'))
        return ts

    @view_config(name='__projector_app_state__.json', renderer='json')
    def app_state(self):
        poll_methods = dict((x.name, x.factory) for x in self.request.registry.registeredAdapters()
                            if x.provided == IPollPlugin)
        poll_groups = [{
            'title': self.request.localizer.translate(g['title']),
            'methods': [{
                'name': m,
                'title': self.request.localizer.translate(poll_methods[m].title),
                'proposalsMin': getattr(poll_methods[m], 'proposals_min', 1),
                'proposalsMax': getattr(poll_methods[m], 'proposals_max', None),
                'rejectProp': reject,
            } for (m, reject) in g['methods'] if m in poll_methods]
        } for g in POLL_GROUPS]
        return {
            'meeting': {
                'href': self.request.resource_path(self.context),
                'title': self.context.title,
                'agenda': [self.serialize_ai(ai) for ai in self._get_ais('ongoing', 'upcoming', 'closed')],
            },
            'pollGroups': poll_groups,
            'ts': self.get_translation_strings(),
            'proposalWorkflowStates': self._get_workflow_states(),
            'api': {
                'quickPoll': self.request.resource_path(self.context, '__quick_poll__.json'),
                'pollIntervalTime': POLL_INTERVAL_TIME,
            },
            'logo': self.request.static_path('voteit.core:static/images/logo.png'),
        }

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

        for uid in self.request.POST.getall('uid[]'):
            prop = self.resolve_uid(uid=uid)
            proposals.append(prop)
            if ai is None:
                ai = prop.__parent__
            else:
                if ai != prop.__parent__:
                    raise HTTPForbidden("Proposals fetched from different agenda items")

        # Poll title might be used by the reject_prop
        poll_title = self.get_quick_poll_title()

        if reject_prop:
            if ai:  # Should be set, otherwise next step will die anyway
                prop = factories['Proposal'](
                    text=translate(_("Reject (for poll ${title})", mapping={'title': poll_title}))
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
        proposal_uids = [x.uid for x in proposals]
        poll = factories['Poll'](
            title=poll_title,
            proposals=proposal_uids,
            poll_plugin=poll_method
        )
        ai[poll.uid] = poll
        poll.set_workflow_state(self.request, 'upcoming')
        poll.set_workflow_state(self.request, 'ongoing')
        return {
            'poll': self.serialize_poll(poll),
            'proposals': [self.serialize_proposal(prop) for prop in proposals],
        }

    def serialize_proposal(self, prop):
        return {
            'uid': prop.uid,
            'aid': prop.aid,
            'text': self.request.render_proposal_text(prop, tag_func=proj_tags2links),
            'workflowState': prop.get_workflow_state(),
            'creator': self.request.creators_info(prop.creator, portrait=False, no_tag=True),
            'workflowApi': self.request.resource_path(prop, '__change_state_projector__.json'),
            'tags': prop.tags,
        }

    @reify
    def voter_count(self):
        return len(tuple(self.request.meeting.local_roles.get_any_local_with(security.ROLE_VOTER)))

    def serialize_poll(self, poll):
        workflow_state = poll.get_workflow_state()
        data = {
            'href': self.request.resource_path(poll, '__show_results__'),
            'title': poll.title,
            'uid': poll.uid,
            'workflowState': workflow_state,
        }
        if workflow_state == 'ongoing':
            data.update({
                'votes': len(poll),
                'api': self.request.resource_path(poll, '__projector_workflow__.json'),
                'potentialVotes': self.voter_count,
            })
        return data

    @view_config(context=IPoll, name="__projector_workflow__.json", renderer='json')
    def set_poll_workflow(self):
        allowed_states = ('closed', 'canceled')
        transl = self.request.localizer.translate
        state = self.request.POST.get('state')
        if state not in allowed_states:
            raise HTTPForbidden(transl(_("Not allowed to transition to ${state}",
                                         mapping={'state': state})))
        self.context.set_workflow_state(self.request, state)
        return self.serialize_poll(self.context)

    # For new reactive projector
    @view_config(context=IAgendaItem, name="__content__.json", renderer='json')
    def agenda_content(self):
        path_query = query.Eq('path', resource_path(self.context))
        prop_query = path_query & query.Eq('type_name', 'Proposal')
        poll_query = path_query & query.Eq('type_name', 'Poll') & query.Any('workflow_state', ('ongoing', 'closed'))
        diff_text = IDiffText(self.context, None)
        tag_order = []
        if diff_text:
            paragraphs = diff_text.get_paragraphs()
            if paragraphs:
                for i in range(1, len(paragraphs) + 1):
                    tag_order.append("%s-%s" % (diff_text.hashtag, i))
        return {
            'proposals': [self.serialize_proposal(x) for x in self.catalog_query(prop_query, resolve=True, perm=None, sort_index='created')],
            'polls':  [self.serialize_poll(poll) for poll in self.catalog_query(poll_query, sort_index='created', resolve=True, perm=None)],
            'agenda': [self.serialize_ai(ai) for ai in self._get_ais('ongoing', 'upcoming', 'closed')],
            'tagOrder': tag_order,  # Javascript names? :P
        }

    @view_config(context=IProposal, name="__change_state_projector__.json", renderer='json')
    def change_state_projector(self):
        """ Change workflow state for context.
            Returns result in json. Only state changes between 'published', 'approved' and 'denied'
            are allowed.
        """
        allowed_states = ('published', 'approved', 'denied')
        transl = self.request.localizer.translate
        state = self.request.POST.get('state')
        if state not in allowed_states:
            raise HTTPForbidden(transl(_("Not allowed to transition to ${state}",
                                         mapping={'state': state})))
        self.context.set_workflow_state(self.request, state)
        return {'status': 'success',
                'state': state}

    def get_quick_poll_title(self):
        poll_query = query.Eq('path', resource_path(self.request.meeting)) & query.Eq('type_name', 'Poll')
        res = self.request.root.catalog.query(poll_query)[0]
        title = _("Descision ${num}", mapping={'num': res.total + 1})
        return self.request.localizer.translate(title)

    @view_config(name="__show_last_poll_result__")
    def show_last_poll_result(self):
        poll_query = query.Eq('type_name', 'Poll') & query.Eq('path', resource_path(self.request.meeting)) & \
                     query.Eq('workflow_state', ['closed'])
        docids = self.request.root.catalog.query(poll_query, sort_index='end_time', limit=1, reverse=True)[1]
        poll = None
        for poll in self.request.resolve_docids(docids):
            break
        if poll:
            return render_view_to_response(poll, self.request, name='__show_results__')
        raise HTTPNotFound(_("No closed polls yet"))


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
