from zope.interface import implements
from BTrees.OOBTree import OOSet

from voteit.core.models.interfaces import IMeeting
from voteit.core.security import ROLE_VOTER

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

    def add(self, userid):
        if self.register_closed:
            #FIXME: translations
            raise Exception(_(u"Electoral register is closed"))

        if userid not in self.register:
            self.register.add(userid)

    def clear(self):
        self.context.__register_closed__ = False
        if hasattr(self.context, '__register__'):
            delattr(self.context, '__register__')
        
        userids_and_groups = []
        for permissions in self.context.get_security():
            groups = list(permissions['groups'])
            if ROLE_VOTER in groups:
                groups.remove(ROLE_VOTER)
            userids_and_groups.append({'userid':permissions['userid'], 'groups':groups})
        
        self.context.set_security(userids_and_groups)

    def close(self):
        self.context.__register_closed__ = True
        register = []
        # remove non numeric userids
        for userid in self.register:
            try:
                int(userid)
                register.append(userid)
            except ValueError:
                pass
        # sort register on userid
        register.sort(key=lambda x: int(x))
        # loop through register starting from 101 and give the first 101 the voter role
        loops = 1
        for userid in register:
            if int(userid) >= 101:
                self.context.add_groups(userid, (ROLE_VOTER, ))
                loops += 1
            if loops > 101:
                break;
