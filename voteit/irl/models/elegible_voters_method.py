from zope.interface import implements
from zope.component import adapts
from voteit.core.models.interfaces import IMeeting

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElegibleVotersMethod


class ElegibleVotersMethod(object):
    name = u'base_method'
    title = u"Subclass to make a new one"
    description = u""
    implements(IElegibleVotersMethod)
    adapts(IMeeting)

    def __init__(self, context):
        """ Context to adapt """
        self.context = context

    def get_voters(self, **kw):
        raise NotImplementedError("Must be implemented by subclass")

