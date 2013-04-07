import unittest

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.meeting import Meeting

from voteit.irl.interfaces import IParticipantNumberClaimed


class ParticipantNumberClaimedTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.events import ParticipantNumberClaimed
        return ParticipantNumberClaimed

    def test_verify_class(self):
        self.assertTrue(verifyClass(IParticipantNumberClaimed, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IParticipantNumberClaimed, self._cut(Meeting(), 22, 'john_doe')))
