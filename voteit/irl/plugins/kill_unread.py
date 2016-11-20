"""
The implemetation with unread in the catalog is built for speed when many users
are connected over a longer timespan.
It's a disaster when many participants try to use the system exactly at once.
Hence this plugin enables a menu item in the cogwheel menu that simply
remove all unread within that AgendaItem

Note: Unread functionality will change in voteit.core
"""
from arche.events import ObjectUpdatedEvent
from arche.interfaces import IFlashMessages
from betahaus.viewcomponent import view_action
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IUnread
from voteit.core.security import MODERATE_MEETING
from zope.component.event import objectEventNotify

from voteit.irl import _


@view_action('context_actions', 'clear_unread',
             title = _("Clear unread"),
             permission = MODERATE_MEETING,
             interface = IAgendaItem)
def change_owner_menu_action(context, request, va, **kw):
    url = request.resource_url(context, '_clear_unread')
    title = request.localizer.translate(va.title)
    return """<li><a href="%s">%s</a></li>""" % (url, title)


@view_config(context = IAgendaItem,
             name = "_clear_unread",
             permission = MODERATE_MEETING)
def kill_unread_view(context, request):
    killed = 0
    for obj in context.values():
        unread = IUnread(obj, None)
        if unread and unread.unread_storage:
            killed += 1
            unread.unread_storage.clear()
            objectEventNotify(ObjectUpdatedEvent(obj, changed=('unread',)))
    fm = IFlashMessages(request, None)
    if fm:
        fm.add(_("Cleared ${num} unread",
                 mapping = {'num': killed}))
    return HTTPFound(location=request.resource_url(context))


def includeme(config):
    config.scan(__name__)
