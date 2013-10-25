from pyramid.events import subscriber
from pyramid.threadlocal import get_current_request

from voteit.irl.interfaces import IParticipantNumberClaimed
from voteit.irl.models.interfaces import IParticipantCallbacks


@subscriber(IParticipantNumberClaimed)
def execute_callers_on_number_claimed(event):
    request = get_current_request()
    callbacks = request.registry.getAdapter(event.meeting, IParticipantCallbacks)
    callbacks.execute_callbacks_for(event.number, event.userid, request = request)
