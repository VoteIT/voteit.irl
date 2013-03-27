from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.decorator import reify
from betahaus.viewcomponent import view_action
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.views.base_view import BaseView

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IParticipantNumbers


class ParticipantNumbersView(BaseView):

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.api.meeting, IParticipantNumbers)

    @view_config(name = "manage_participant_numbers", context = IMeeting, permission = security.MODERATE_MEETING,
                 renderer = "templates/participant_numbers.pt")
    def manage_participant_numbers(self):
        if 'back' in self.request.POST:
            return HTTPFound(location = self.api.meeting_url)
        add = 'add' in self.request.POST
        remove = 'remove' in self.request.POST
        if add or remove:
            #Basic validation
            try:
                start = self.request.POST.get('start', None)
                start = int(start)
                end = self.request.POST.get('end', None)
                if not end:
                    end = None
                else:
                    end = int(end)
                    if start > end:
                        raise HTTPForbidden(_(u"End must be higher than start"))
            except TypeError:
                raise HTTPForbidden(_(u"Must be an integer value"))
            if add:
                res = self.participant_numbers.new_tickets(self.api.userid, start, end)
                msg = _(u"Added ${count} new numbers",
                        mapping = {'count': len(res)})
            if remove:
                res = self.participant_numbers.clear_numbers(start, end)
                msg = _(u"Removed ${count} numbers",
                        mapping = {'count': len(res)})
            self.api.flash_messages.add(msg)
            here_url = self.request.resource_url(self.context, 'manage_participant_numbers')
            return HTTPFound(location = here_url)
        self.response['participant_numbers'] = self.participant_numbers
        return self.response


@view_action('meeting', 'participant_numbers', permission = security.MODERATE_MEETING)
def participant_numbers_menu(context, request, va, **kw):
    api = kw['api']
    return """<li><a href="%s">%s</a></li>""" % ("%s/manage_participant_numbers" % api.meeting_url,
                                                 api.translate(_(u"Participant numbers")))