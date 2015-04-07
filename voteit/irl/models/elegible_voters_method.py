from __future__ import unicode_literals

from zope.interface import implementer
from zope.component import adapter
from voteit.core.models.interfaces import IMeeting

from voteit.irl import _
from voteit.irl.models.interfaces import IElegibleVotersMethod


@implementer(IElegibleVotersMethod)
@adapter(IMeeting)
class ElegibleVotersMethod(object):
    """ Abstract class - subclass this one to make an elegible voters method.
        See IElegibleVotersMethod for docs.
    """
    name = ''
    title = "Subclass to make a new one"
    description = ""

    def __init__(self, context):
        self.context = context

    def get_voters(self, request = None, **kw):
        raise NotImplementedError("Must be implemented by subclass")
