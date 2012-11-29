from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.decorator import reify
from pyramid.response import Response
from pyramid.renderers import render
from betahaus.viewcomponent import view_action

from voteit.core.models.interfaces import IMeeting
from voteit.core.views.base_view import BaseView
from voteit.core.security import VIEW
from voteit.core.security import MODERATE_MEETING

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.fanstaticlib import voteit_irl_set_as_present
from voteit.irl.models.interfaces import IMeetingPresence


class MeetingPresenceView(BaseView):

    @reify
    def mp_util(self):
        """ Note that this only works for IMeeting views. Change this later if we need to update. """
        return self.request.registry.getAdapter(self.context, IMeetingPresence)

    @view_config(name="register_meeting_presence", context=IMeeting, permission=VIEW,
                 renderer = "templates/register_meeting_presence.pt")
    def register_meeting_presence(self):
        """ Controls for setting yourself as present
        """
        voteit_irl_set_as_present.need()
        self.response['current'] = self.register_current_status()
        return self.response

    def register_current_status(self):
        self.response['mp_util'] = self.mp_util
        self.response['is_registered'] = self.api.userid in self.mp_util.present_userids
        return render("templates/meeting_presence_status.pt", self.response, request = self.request)

    @view_config(name="_register_set_attending", context=IMeeting, permission=VIEW, xhr=True)
    def register_set_attending(self):
        assert self.api.userid
        self.mp_util.add(self.api.userid)
        return Response(self.register_current_status())

    @view_config(name="_toggle_presence_check", context=IMeeting, permission=MODERATE_MEETING)
    def toggle_open_presence_check(self):
        if self.mp_util.open:
            self.mp_util.end_check()
        else:
            self.mp_util.start_check()
        url = self.request.resource_url(self.api.meeting, 'register_meeting_presence')
        return HTTPFound(location = url)


@view_action('participants_menu', 'register_meeting_presence', title = _(u"Meeting presence"))
def meeting_presence_link(context, request, va, **kw):
    api = kw['api']
    if not api.userid or not api.meeting:
        return ''
    link = request.resource_url(api.meeting, 'register_meeting_presence')
    return """ <li class="tab"><a href="%s">%s</a></li>"""  % (link, api.translate(va.title))
