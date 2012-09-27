from copy import deepcopy

from zope.interface import implements

from voteit.core.security import ROLE_VOTER

from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElectoralRegisterMethod


class ElectoralRegisterMethod(object):
    name = 'standard_electoral_register_method'
    title = _(u"standard_electoral_register_method_description", default=u"Standard method")
    description = _(u"standard_electoral_register_method_description",
                    default = u"")
    implements(IElectoralRegisterMethod)
    
    def __init__(self, context):
        """ Context to adapt """
        self.context = context

    def apply(self, userids):
        # removing ROLE_VOTER from all users
        userids_and_groups = []
        for permissions in self.context.get_security():
            groups = list(permissions['groups'])
            if ROLE_VOTER in groups:
                groups.remove(ROLE_VOTER)
            userids_and_groups.append({'userid':permissions['userid'], 'groups':groups})
        
        self.context.set_security(userids_and_groups, event=False)
        
        # set ROLE_VOTER on all users in userids
        for userid in userids:
            self.context.add_groups(userid, (ROLE_VOTER, ), event=False)