from arche.views.base import BaseView
from betahaus.viewcomponent import view_action
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.response import Response
from pyramid.view import view_config
from voteit.core.models.interfaces import IMeeting
from voteit.core.security import MODERATE_MEETING
from voteit.core.security import VIEW

from voteit.irl import _
from voteit.irl.fanstaticlib import voteit_irl_set_as_present
from voteit.irl.models.interfaces import IMeetingPresence


#FIXME: REFACTOR THIS

class MeetingPresenceView(BaseView):

    @reify
    def mp_util(self):
        """ Note that this only works for IMeeting views. Change this later if we need to update. """
        return self.request.registry.getAdapter(self.context, IMeetingPresence)

    @view_config(name = "register_meeting_presence",
                 context=IMeeting, permission=VIEW,
                 renderer = "voteit.irl:templates/register_meeting_presence.pt")
    def register_meeting_presence(self):
        """ Controls for setting yourself as present
        """
        voteit_irl_set_as_present.need()
        return {'current': self.register_current_status()}

    def register_current_status(self):
        response = {}
        response['mp_util'] = self.mp_util
        response['is_registered'] = self.request.authenticated_userid in self.mp_util.present_userids
        return render("voteit.irl:templates/meeting_presence_status.pt", response, request = self.request)

    @view_config(name = "_register_set_attending", context = IMeeting, permission = VIEW)
    def register_set_attending(self):
        assert self.request.authenticated_userid
        self.mp_util.add(self.request.authenticated_userid)
        if self.request.is_xhr:
            return Response(self.register_current_status())
        url = self.request.resource_url(self.context, 'register_meeting_presence')
        return HTTPFound(location = url)

    @view_config(name = "_toggle_presence_check", context = IMeeting, permission = MODERATE_MEETING)
    def toggle_open_presence_check(self):
        if self.mp_util.open:
            self.mp_util.end_check()
        else:
            self.mp_util.start_check()
        url = self.request.resource_url(self.context, 'register_meeting_presence')
        return HTTPFound(location = url)


@view_action('participants_menu', 'register_meeting_presence',
             title = _("Meeting presence"))
def meeting_presence_link(context, request, va, **kw):
    if not request.authenticated_userid or not request.meeting:
        return ''
    link = request.resource_url(request.meeting, 'register_meeting_presence')
    return """ <li><a href="%s">%s</a></li>"""  % (link, request.localizer.translate(va.title))
