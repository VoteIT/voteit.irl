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
        
        obj.add('robin')
        obj.add('kalle')
        
        obj.close()
        self.assertTrue(obj.register_closed)
        
        self.assertTrue(obj.context.__register_closed__)
        self.assertEqual(len(obj.archive), 1)
        self.assertIn('robin', obj.archive['1']['userids'])
        self.assertIn('kalle', obj.archive['1']['userids'])

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

    def test_add_archive(self):
        obj = self._make_adapted_obj()
        
        obj.add_archive(ALL_TEST_USERS)
        
        self.assertEqual(len(obj.archive), 1)
        self.assertIn('robin', obj.archive['1']['userids'])
        self.assertIn('anders', obj.archive['1']['userids'])
        