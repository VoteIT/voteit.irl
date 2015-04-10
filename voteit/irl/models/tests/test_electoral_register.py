import unittest
from datetime import datetime

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass

from voteit.irl.models.interfaces import IElectoralRegister


class ElectoralRegisterTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.electoral_register import ElectoralRegister
        return ElectoralRegister

    @property
    def _meeting(self):
        from voteit.core.models.meeting import Meeting
        return Meeting

    def test_verify_class(self):
        self.assertTrue(verifyClass(IElectoralRegister, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IElectoralRegister, self._cut(self._meeting())))

    def test_current(self):
        obj = self._cut(self._meeting())
        self.assertEqual(obj.current, None)
        obj.new_register(['1', '2'])
        self.failUnless(obj.current)

    def test_get_next_key(self):
        obj = self._cut(self._meeting())
        self.assertEqual(obj.get_next_key(), 0)
        obj.registers[10] = 'Dummy'
        self.assertEqual(obj.get_next_key(), 11)

    def test_currently_set_voters(self):
        self.config.include('arche.testing')
        meeting = self._meeting()
        meeting.local_roles.add('john', ['role:Voter'])
        meeting.local_roles.add('jane', ['role:Voter'])
        meeting.local_roles.add('doe', ['role:Voter'])
        meeting.local_roles.add('jeff', ['role:Viewer'])
        meeting.local_roles.add('janet', ['role:Viewer'])
        obj = self._cut(meeting)
        self.assertEqual(obj.currently_set_voters(), frozenset(['john', 'jane', 'doe']))

    def test_new_register(self):
        obj = self._cut(self._meeting())
        obj.new_register(['hello', 'world'])
        self.assertEqual(len(obj.registers), 1)
        self.assertEqual(obj.registers[0]['userids'], frozenset(['hello', 'world']))
        self.assertIsInstance(obj.registers[0]['time'], datetime)

    def test_new_register_needed(self):
        self.config.include('arche.testing')
        meeting = self._meeting()
        obj = self._cut(meeting)
        self.assertTrue(obj.new_register_needed())
        meeting.local_roles.add('john', ['role:Voter'])
        self.assertTrue(obj.new_register_needed())
        obj.new_register(['john'])
        self.assertFalse(obj.new_register_needed())
        meeting.local_roles.add('jane', ['role:Voter'])
        self.assertTrue(obj.new_register_needed())
