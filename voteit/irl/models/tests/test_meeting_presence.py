import unittest
from datetime import datetime

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from pyramid.httpexceptions import HTTPForbidden

from voteit.irl.models.interfaces import IMeetingPresence


class MeetingPresenceTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.meeting_presence import MeetingPresence
        return MeetingPresence

    def test_verify_class(self):
        self.assertTrue(verifyClass(IMeetingPresence, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IMeetingPresence, self._cut()))

    def test_add_when_open(self):
        obj = self._cut()
        obj.start_check()
        obj.add('hello')

    def test_add_when_closed(self):
        obj = self._cut()
        self.assertRaises(HTTPForbidden, obj.add, 'valid')

    def test_add_bad_type(self):
        obj = self._cut()
        obj.start_check()
        self.assertRaises(AssertionError, obj.add, 1)

    def test_start_sets_start_time(self):
        obj = self._cut()
        obj.start_check()
        self.assertIsInstance(obj.start_time, datetime)
        
    def test_end_sets_end_time(self):
        obj = self._cut()
        obj.start_check()
        self.assertEqual(obj.end_time, None)
        obj.end_check()
        self.assertIsInstance(obj.end_time, datetime)

        