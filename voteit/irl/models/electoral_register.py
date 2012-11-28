from copy import deepcopy

from zope.interface import implements
from zope.component import adapts
from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree
from voteit.core.models.date_time_util import utcnow
from voteit.core.models.interfaces import IMeeting
from voteit.core.security import ROLE_VOTER


from voteit.irl import VoteIT_IRL_MF as _
from voteit.irl.models.interfaces import IElectoralRegister


class ElectoralRegister(object):
    __doc__ = IElectoralRegister.__doc__
    implements(IElectoralRegister)
    adapts(IMeeting)
    
    def __init__(self, context):
        self.context = context

    @property
    def registers(self):
        try:
            return self.context.__electoral_registers__
        except AttributeError:
            self.context.__electoral_registers__ = IOBTree()
            return self.context.__electoral_registers__

    @property
    def current(self):
        try:
            return self.registers[self.registers.maxKey()]
        except ValueError: #When empty
            return

    def get_next_key(self):
        if len(self.registers):
            return self.registers.maxKey() + 1
        else:
            return 0

    def currently_set_voters(self):
        userids = set()
        for item in self.context.get_security():
            if ROLE_VOTER in item['groups']:
                userids.add(item['userid'])
        return frozenset(userids)

    def new_register(self, userids):
        reg = OOBTree()
        reg.update({'userids': frozenset(userids), 'time': utcnow()})
        self.registers[self.get_next_key()] = reg

    def new_register_needed(self):
        if not self.current:
            return True
        return self.current['userids'] != self.currently_set_voters()
