import unittest

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass

from voteit.irl.models.interfaces import IElegibleVotersMethod


class ElegibleVotersMethodTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.elegible_voters_method import ElegibleVotersMethod
        return ElegibleVotersMethod

    @property
    def _meeting(self):
        from voteit.core.models.meeting import Meeting
        return Meeting

    def test_verify_class(self):
        self.assertTrue(verifyClass(IElegibleVotersMethod, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IElegibleVotersMethod, self._cut(self._meeting())))
