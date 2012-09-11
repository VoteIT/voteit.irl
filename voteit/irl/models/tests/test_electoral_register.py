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
        from voteit.core.models.meeting import Meeting
        self.meeting = Meeting()
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
        
        obj.add('50')
        obj.add('150')
        obj.add('250')
        
        obj.close()
        self.assertTrue(obj.register_closed)
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('50'))
        self.assertTrue('role:Voter' in self.meeting.get_groups('150'))
        self.assertTrue('role:Voter' in self.meeting.get_groups('250'))

    def test_clear(self):
        obj = self._make_adapted_obj()
        obj.context.__register_closed__ = False
        
        obj.add('fredrik')
        obj.add('robin')
        obj.add('anders')
        
        obj.close()
        
        obj.clear()
        self.assertFalse(obj.register_closed)
        self.assertEqual(len(obj.register), 0)
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('fredrik'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('robin'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('anders'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('hanna'))
        
    def test_sverok_all_delegates(self):
        obj = self._make_adapted_obj()
        obj.context.__register_closed__ = False
        
        obj.add('admin')
        
        # delegates
        for n in range(101, 202):
            obj.add("%s" % n)
        
        # reserves
        for n in range(202, 298):
            obj.add("%s" % n)
        
        # clerks
        for n in range(1, 54):
            obj.add("%s" % n)
        
        obj.close()
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('admin'))
        
        self.assertTrue('role:Voter' in self.meeting.get_groups('101'))
        self.assertTrue('role:Voter' in self.meeting.get_groups('201'))
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('202'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('297'))
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('1'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('53'))
        
    def test_sverok_missing_delegates(self):
        obj = self._make_adapted_obj()
        obj.context.__register_closed__ = False
        
        obj.add('admin')
        
        # delegates
        for n in range(101, 200):
            obj.add("%s" % n)
        
        # reserves
        for n in range(202, 298):
            obj.add("%s" % n)
        
        # clerks
        for n in range(1, 54):
            obj.add("%s" % n)
        
        obj.close()
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('admin'))
        
        self.assertTrue('role:Voter' in self.meeting.get_groups('101'))
        self.assertTrue('role:Voter' in self.meeting.get_groups('199'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('200'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('201'))
        
        self.assertTrue('role:Voter' in self.meeting.get_groups('202'))
        self.assertTrue('role:Voter' in self.meeting.get_groups('203'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('204'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('297'))
        
        self.assertFalse('role:Voter' in self.meeting.get_groups('1'))
        self.assertFalse('role:Voter' in self.meeting.get_groups('53'))
