from zope.interface import implements
from BTrees.OOBTree import OOSet


from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IEligibleVoters


class EligibleVoters(object):
    __doc__ = IEligibleVoters.__doc__
    implements(IEligibleVoters)
    
    def __init__(self, context):
        """ Context to adapt """
        self.context = context

    @property
    def list(self):
        try:
            return self.context.__eligible_voters__
        except AttributeError:
            self.context.__eligible_voters__ = OOSet()
            return self.context.__eligible_voters__