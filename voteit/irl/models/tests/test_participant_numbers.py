import unittest
from datetime import datetime

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.meeting import Meeting

from voteit.irl.models.interfaces import IParticipantNumbers


class ParticipantNumbersTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.participant_numbers import ParticipantNumbers
        return ParticipantNumbers

    def test_verify_class(self):
        self.assertTrue(verifyClass(IParticipantNumbers, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IParticipantNumbers, self._cut(Meeting())))

    def test_new_tickets(self):
        obj = self._cut(testing.DummyResource())
        res = obj.new_tickets(0)
        self.assertEqual(res, [0])
        self.assertEqual(len(obj.tickets), 1)
        token = obj.tickets[0].token
        self.assertEqual(len(obj.userid_to_number), 0)
        self.assertEqual(len(obj.number_to_userid), 0)
        self.assertIn(token, obj.token_to_number)
        self.assertEqual(0, obj.token_to_number[token])

    def test_new_tickets_several(self):
        obj = self._cut(testing.DummyResource())
        res = obj.new_tickets(0, 9)
        self.assertEqual(len(res), 10)
        self.assertEqual(len(obj.tickets), 10)

    def test_new_tickets_with_existing(self):
        obj = self._cut(testing.DummyResource())
        res = obj.new_tickets(5, 7)
        self.assertEqual(len(res), 3)
        res = obj.new_tickets(1, 10)
        self.assertEqual(len(res), 7)
        self.assertEqual(len(obj.tickets), 10)

    def test_claim_ticket(self):
        obj = self._cut(testing.DummyResource())
        obj.new_tickets(0)
        ticket = obj.tickets[0]
        token = ticket.token
        obj.claim_ticket('jeff', token)
        self.assertIsInstance(ticket.claimed, datetime)
        self.assertEqual(ticket.claimed_by, 'jeff')
        self.assertEqual(len(obj.userid_to_number), 1)
        self.assertEqual(len(obj.number_to_userid), 1)
        self.assertEqual(obj.userid_to_number['jeff'], 0)
        self.assertEqual(obj.number_to_userid[0], 'jeff')

    def test_clear_number(self):
        obj = self._cut(testing.DummyResource())
        obj.new_tickets(0, 1)
        obj.clear_number(0)
        self.assertEqual(len(obj.tickets), 1)
        self.assertNotIn(0, obj.tickets)
        self.assertNotIn(0, obj.token_to_number.values())

    def test_clear_numbers(self):
        obj = self._cut(testing.DummyResource())
        obj.new_tickets(0, 5)
        res = obj.clear_numbers(1, 3)
        self.assertEqual(len(res), 3)
        self.assertEqual(len(obj.tickets), 3)
        self.assertIn(0, obj.tickets)
        self.assertNotIn(1, obj.tickets)
        self.assertNotIn(2, obj.tickets)
        self.assertNotIn(3, obj.tickets)
        self.assertIn(4, obj.tickets)
        self.assertIn(5, obj.tickets)

    def test_clear_numbers_with_some_gaps(self):
        obj = self._cut(testing.DummyResource())
        obj.new_tickets(1, 5)
        res = obj.clear_numbers(1)
        self.assertEqual(len(res), 1)
        self.assertEqual(len(obj.tickets), 4)
        res = obj.clear_numbers(0, 10)
        self.assertEqual(len(res), 4)
        self.assertEqual(len(obj.tickets), 0)

    def test_clear_numbers_removes_userdata_too(self):
        obj = self._cut(testing.DummyResource())
        obj.new_tickets(1, 5)
        obj.claim_ticket('jane', obj.tickets[1].token)
        obj.claim_ticket('joe', obj.tickets[2].token)
        obj.claim_ticket('jeff', obj.tickets[3].token)
        self.assertEqual(len(obj.userid_to_number), 3)
        self.assertEqual(len(obj.number_to_userid), 3)
        self.assertEqual(len(obj.tickets), 5)
        self.assertEqual(len(obj.token_to_number), 5)
        res = obj.clear_numbers(1, 2)
        self.assertEqual(len(res), 2)
        self.assertEqual(len(obj.userid_to_number), 1)
        self.assertEqual(len(obj.number_to_userid), 1)
        self.assertEqual(len(obj.tickets), 3)
        self.assertEqual(len(obj.token_to_number), 3)

    def test_claim_ticket_already_claimed(self):
        from voteit.irl.models.participant_numbers import TicketAlreadyClaimedError
        obj = self._cut(testing.DummyResource())
        obj.new_tickets(1)
        token = obj.tickets[1].token
        obj.claim_ticket('jane', token)
        self.assertRaises(TicketAlreadyClaimedError, obj.claim_ticket, 'dummy', token)
        