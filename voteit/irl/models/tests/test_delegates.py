import unittest

from pyramid import testing
from zope.interface.verify import verifyObject


class DelegatesTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _make_adapted_obj(self):
        from voteit.irl.models.delegates import Delegates
        from voteit.core.models.meeting import Meeting
        self.meeting = Meeting()
        return Delegates(self.meeting)

    def test_interface(self):
        from voteit.irl.models.interfaces import IDelegates
        obj = self._make_adapted_obj()
        self.assertTrue(verifyObject(IDelegates, obj))

    def test_add(self):
        obj = self._make_adapted_obj()
        obj.list.add('robin')
        self.assertTrue('robin' in obj.list)
        obj.list.add('robin')
        self.assertEqual(len(obj.list), 1)
        
    def test_remove(self):
        obj = self._make_adapted_obj()
        obj.list.add('robin')
        self.assertTrue('robin' in obj.list)
        obj.list.remove('robin')
        self.assertFalse('robin' in obj.list)
