from copy import deepcopy

from zope.interface import implements
from BTrees.OOBTree import OOSet, OOBTree

from voteit.core.models.date_time_util import utcnow

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElectoralRegister


class ElectoralRegister(object):
    __doc__ = IElectoralRegister.__doc__
    implements(IElectoralRegister)
    
    def __init__(self, context):
        """ Context to adapt """
        self.context = context

    @property
    def register(self):
        try:
            return self.context.__register__
        except AttributeError:
            self.context.__register__ = OOSet()
            return self.context.__register__

    @property
    def register_closed(self):
        try:
            return self.context.__register_closed__
        except AttributeError:
            self.context.__register_closed__ = True
            return self.context.__register_closed__
        
    @property
    def archive(self):
        try:
            return self.context.__archive__
        except AttributeError:
            self.context.__archive__ = OOBTree()
            return self.context.__archive__

    def add(self, userid):
        if self.register_closed:
            raise Exception(_(u"Electoral register is closed"))

        self.register.add(userid)

    def clear(self):
        self.context.__register_closed__ = False
        if hasattr(self.context, '__register__'):
            delattr(self.context, '__register__')        

    def close(self):
        self.context.__register_closed__ = True

        self.add_archive(deepcopy(self.register))
        
    def add_archive(self, userids):
        #FIXME: This should be an int key and it should check maxKey
        #Refactor and do a migration
        id = "%s" % (len(self.archive)+1)
        self.archive[id] = {'time': utcnow(), 'userids': OOSet(userids)}
