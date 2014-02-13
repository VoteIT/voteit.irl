from zope.interface import implementer
from zope.component import adapter
from voteit.core.models.interfaces import IMeeting

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElegibleVotersMethod


@implementer(IElegibleVotersMethod)
@adapter(IMeeting)
class ElegibleVotersMethod(object):
    """ Abstract class - subclass this one to make an elegible voters method.
        See IElegibleVotersMethod for docs.
    """
    name = u'base_method'
    title = u"Subclass to make a new one"
    description = u""

    def __init__(self, context):
        self.context = context

    def get_voters(self, **kw):
        raise NotImplementedError("Must be implemented by subclass")
