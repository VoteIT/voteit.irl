import unittest

from pyramid import testing
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from zope.interface.verify import verifyObject


ALL_TEST_USERS = set(('fredrik', 'anders', 'hanna', 'robin', 'admin'))

class ElectoralRegisterTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _make_adapted_obj(self):
        from voteit.irl.models.electoral_register import ElectoralRegister
        from voteit.irl.models.eligible_voters import EligibleVoters
        from voteit.core.models.meeting import Meeting
        self.meeting = Meeting()
        eligible_voters = EligibleVoters(self.meeting)
        eligible_voters.list.update(ALL_TEST_USERS)
        return ElectoralRegister(self.meeting)

    def test_interface(self):
        from voteit.irl.models.interfaces import IElectoralRegister
        obj = self._make_adapted_obj()
        self.assertTrue(verifyObject(IElectoralRegister, obj))

    def test_add(self):
        obj = self._make_adapted_obj()
        obj.context.__register_closed__ = False
        obj.add('robin')
        self.failUnless('robin' in obj.register)
        obj.add('robin')
        self.assertEqual(len(obj.register), 1)
        
    def test_close(self):
        obj = self._make_adapted_obj()
        obj.context.__register_closed__ = False
        
        obj.add('robin')
        obj.add('kalle')
        
        obj.close()
        self.assertTrue(obj.register_closed)
        
        self.assertTrue(obj.context.__register_closed__)
        self.assertTrue('role:Voter' in self.meeting.get_groups('robin'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('kalle'))

    def test_clear(self):
        obj = self._make_adapted_obj()
        obj.context.__register_closed__ = False
        
        obj.add('fredrik')
        obj.add('robin')
        obj.add('anders')
        obj.add('kalle')
        
        obj.close()
        
        obj.clear()
        self.assertFalse(obj.register_closed)
        self.assertEqual(len(obj.register), 0)
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('fredrik'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('robin'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('anders'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('hanna'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('kalle'))
