from zope.interface import implements
from BTrees.OOBTree import OOSet


from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IDelegates


class Delegates(object):
    __doc__ = IDelegates.__doc__
    implements(IDelegates)
    
    def __init__(self, context):
        """ Context to adapt """
        self.context = context

    @property
    def list(self):
        try:
            return self.context.__delegates__
        except AttributeError:
            self.context.__delegates__ = OOSet()
            return self.context.__delegates__