import deform
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.decorator import reify
from pyramid.security import NO_PERMISSION_REQUIRED
from betahaus.viewcomponent import view_action
from betahaus.pyracont.factories import createSchema
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.views.base_view import BaseView

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IParticipantCallback
from voteit.irl.models.interfaces import IParticipantCallbacks
from voteit.irl.models.interfaces import IParticipantNumbers


class ParticipantCallbacksView(BaseView):

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.api.meeting, IParticipantNumbers)

    @reify
    def participant_callbacks(self):
        return self.request.registry.getAdapter(self.api.meeting, IParticipantCallbacks)

#    @view_config(name = "manage_participant_callbacks", context = IMeeting, permission = security.MODERATE_MEETING,
#                 renderer = "templates/participant_callbacks.pt")
    def manage_participant_callbacks(self):
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
            
            callback = self.request.POST['callback']
            #FIXME: Validate, check that an adapter exists
            if add:
                added, existed = self.participant_callbacks.add(callback, start, end)
                msg = _(u"Added ${added} new callbacks and skipped ${existed} that already existed.",
                        mapping = {'added': len(added), 'existed': len(existed)})
                self.api.flash_messages.add(msg)
                if self.request.POST.get('execute_for_existing', True):
                    callback_adapter = self.request.registry.getAdapter(self.api.meeting, IParticipantCallback, name = callback)
                    executed = 0
                    if end == None:
                        end = start
                    for i in range(start, end + 1): #Range  stops before end otherwise
                        if i in self.participant_numbers.number_to_userid:
                            callback_adapter(i, self.participant_numbers.number_to_userid[i])
                            executed += 1
                    msg = _(u"Executed callback for ${num} users that had already claimed a participant number.",
                            mapping = {'num': executed})
                    self.api.flash_messages.add(msg)
            if remove:
                removed, nonexistent = self.participant_callbacks.remove(callback, start, end)
                msg = _(u"Removed ${removed} callbacks and skipped ${nonexistent} that wasn't registered.",
                        mapping = {'removed': len(removed), 'nonexistent': len(nonexistent)})
                self.api.flash_messages.add(msg)
            here_url = self.request.resource_url(self.context, 'manage_participant_callbacks')
            return HTTPFound(location = here_url)
        self.response['participant_numbers'] = self.participant_numbers
        self.response['participant_callbacks'] = self.participant_callbacks
        self.response['callback_adapters'] = [adapter for (name, adapter) in self.request.registry.getAdapters([self.api.meeting], IParticipantCallback)]
        return self.response


#@view_action('meeting', 'participant_callbacks', permission = security.MODERATE_MEETING)
def participant_callbacks_menu(context, request, va, **kw):
    api = kw['api']
    return """<li><a href="%s">%s</a></li>""" % ("%smanage_participant_callbacks" % api.meeting_url,
                                                 api.translate(_(u"Participant callbacks")))
