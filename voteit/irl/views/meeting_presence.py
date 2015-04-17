from arche.portlets import PortletType
from arche.views.base import BaseView
from betahaus.viewcomponent import view_action
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.view import view_config
from pyramid.view import view_defaults
from voteit.core.helpers import get_meeting_participants
from voteit.core.models.interfaces import IMeeting
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import VIEW

from voteit.irl import _
from voteit.irl.fanstaticlib import meeting_presence_moderator
from voteit.irl.models.interfaces import IMeetingPresence
from voteit.irl.models.interfaces import IParticipantNumbers


class MeetingPresencePortlet(PortletType):
    name = "meeting_presence_portlet"
    title = "Meeting Presence"

    def __init__(self, portlet):
        self.portlet = portlet

    def render(self, context, request, view, **kwargs):
        if request.meeting and request.is_moderator:
            mp_util = request.registry.getAdapter(request.meeting, IMeetingPresence)
            response = {'title': self.title,
                        'portlet': self.portlet,
                        'mp_util': mp_util,
                        'view': view,}
            if mp_util.open:
                meeting_presence_moderator.need()
                response['participants_count'] = len(get_meeting_participants(context))
            return render("voteit.irl:templates/meeting_presence.pt",
                          response,
                          request = request)


@view_defaults(context = IMeeting, permission = VIEW)
class MeetingPresenceView(BaseView):
 
    @reify
    def mp_util(self):
        """ Note that this only works for IMeeting views. Change this later if we need to update. """
        return self.request.registry.getAdapter(self.context, IMeetingPresence)

    @view_config(name = "meeting_presence.json",
                 permission = MODERATE_MEETING)
    def presence_data_json(self):
        response = {}
        response['present_count'] = len(self.mp_util.present_userids)
        return response

    @view_config(name = "_presence_check_ctrl",
                 permission = MODERATE_MEETING,
                 renderer = 'json')
    def presence_check_ctrl(self):
        action = self.request.GET.get('action', '')
        if action == 'start':
            self.flash_messages.add(_("Started"), type = 'success')
            self.mp_util.start_check()
        elif action == 'end':
            self.flash_messages.add(_("Closed"), type = 'warning')
            self.mp_util.end_check()
        else:
            raise HTTPForbidden("No such action %r" % action)
        came_from = self.request.GET.get('came_from', self.request.resource_url(self.request.meeting))
        return HTTPFound(location = came_from)

    @view_config(name = "_set_as_present",
                 renderer = 'voteit.irl:templates/register_presence_done.pt',
                 permission = VIEW)
    def set_as_present(self):
        if self.request.authenticated_userid not in self.mp_util.present_userids:
            #Add here will raise forbidden if it isn't open
            self.mp_util.add(self.request.authenticated_userid)
        if self.request.is_xhr:
            return {}
        self.flash_messages.add(_("You're now set as present"), type = 'success')
        return HTTPFound(localtion = self.request.resource_url(self.request.meeting))

    @view_config(name = "_add_as_present",
                 renderer = 'json',
                 permission = MODERATE_MEETING,
                 xhr = True)
    def add_as_present(self):
        if not self.mp_util.open:
            return {'status': 'error',
                    'msg': _("Check not open")}
        userid_or_pn = self.request.POST.get('userid_or_pn', '')
        pn = None
        try:
            pn = int(userid_or_pn)
        except ValueError:
            #User is probably a userid
            pass
        transl = self.request.localizer.translate
        if isinstance(pn, int):
            pns = IParticipantNumbers(self.context)
            userid = pns.number_to_userid.get(pn, None)
            if userid is None:
                msg = _("No user with number: '${num}'",
                        mapping = {'num': pn})
                return {'status': 'error',
                        'msg': transl(msg)}
        else:
            userid = userid_or_pn
        user = self.root['users'].get(userid, None)
        if not user:
            msg = _("User not found: '${userid}'",
                    mapping = {'userid': userid})
            return {'status': 'error',
                    'msg': transl(msg)}
        if userid not in self.mp_util.present_userids:
            self.mp_util.add(userid)
            return {'status': 'success',
                    'count': len(self.mp_util.present_userids),
                    'msg': transl(_("Added ${userid}", mapping = {'userid': userid}))}
        else:
            return {'status': 'warning',
                    'msg': transl(_("Already registered: ${userid}",
                                    mapping = {'userid': userid}))}

    @view_config(name = "present_userids",
                 permission = MODERATE_MEETING,
                 renderer = "voteit.irl:templates/meeting_presence_userids.pt")
    def view_userids(self):
        return {'userids': self.mp_util.present_userids}


@view_action('watcher_json', 'meeting_presence')
def meeting_presence_json(context, request, va, **kw):
    """ Return the status of meeting presence checks.
        Can be: open, closed, confirmed, where confirmed is when it's open
        and the current user have confirmed their presence.
    """
    meeting_presence = request.registry.getAdapter(context, IMeetingPresence)
    response = {}
    if meeting_presence.open:
        if request.authenticated_userid in meeting_presence.present_userids:
            response['status'] = 'confirmed'
            return response
        response['status'] = 'open'
        response['msg'] = render('voteit.irl:templates/register_presence.pt', {}, request = request)
        return response
    response['status'] = 'closed'
    return response

@view_action('watcher_json', 'meeting_presence_count')
def meeting_presence_count_json(context, request, va, **kw):
    """ Return number of users who've registered themselves."""
    if request.is_moderator:
        meeting_presence = request.registry.getAdapter(context, IMeetingPresence)
        if meeting_presence.open:
            return len(meeting_presence.present_userids)


def includeme(config):
    config.add_portlet(MeetingPresencePortlet)
