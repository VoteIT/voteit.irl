from __future__ import unicode_literals

from arche.views.base import BaseView
from betahaus.viewcomponent import view_action
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
import deform

from voteit.irl import _
from voteit.irl.models.interfaces import IParticipantCallback
from voteit.irl.models.interfaces import IParticipantCallbacks
from voteit.irl.models.interfaces import IParticipantNumbers


class ParticipantCallbacksView(BaseView):

    @reify
    def participant_numbers(self):
        return self.request.registry.getAdapter(self.context, IParticipantNumbers)

    @reify
    def participant_callbacks(self):
        return self.request.registry.getAdapter(self.context, IParticipantCallbacks)

    @view_config(name = "manage_participant_callbacks",
                 context = IMeeting,
                 permission = security.MODERATE_MEETING,
                 renderer = "voteit.irl:templates/participant_callbacks.pt")
    def manage_participant_callbacks(self):
        if 'back' in self.request.POST:
            return HTTPFound(location = self.request.resource_url(self.context))
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
                        raise HTTPForbidden(_("End must be higher than start"))
            except TypeError:
                raise HTTPForbidden(_("Must be an integer value"))
            
            callback = self.request.POST['callback']
            if add:
                added, existed = self.participant_callbacks.add(callback, start, end)
                msg = _(u"Added ${added} new callbacks and skipped ${existed} that already existed.",
                        mapping = {'added': len(added), 'existed': len(existed)})
                self.flash_messages.add(msg)
                if self.request.POST.get('execute_for_existing', True):
                    executed = 0
                    if end == None:
                        end = start
                    for i in range(start, end + 1): #Range  stops before end otherwise
                        if i in self.participant_numbers.number_to_userid:
                            #The method execute_callbacks_for is fault tolerant for missing callbacks, but not for
                            #failures within the actual callback.
                            self.participant_callbacks.execute_callbacks_for(i, self.participant_numbers.number_to_userid[i],
                                                                             limit = callback, request = self.request)
                            executed += 1
                    msg = _(u"Executed callback for ${num} users that had already claimed a participant number.",
                            mapping = {'num': executed})
                    self.flash_messages.add(msg)
            if remove:
                removed, nonexistent = self.participant_callbacks.remove(callback, start, end)
                msg = _(u"Removed ${removed} callbacks and skipped ${nonexistent} that wasn't registered.",
                        mapping = {'removed': len(removed), 'nonexistent': len(nonexistent)})
                self.flash_messages.add(msg)
            here_url = self.request.resource_url(self.context, 'manage_participant_callbacks')
            return HTTPFound(location = here_url)
        response = {}
        response['participant_numbers'] = self.participant_numbers
        response['participant_callbacks'] = self.participant_callbacks
        response['callback_adapters'] = [adapter for (name, adapter) in self.request.registry.getAdapters([self.request.meeting], IParticipantCallback)]
        return response
