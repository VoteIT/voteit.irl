from unittest import TestCase

from pyramid import testing
from voteit.core.models.agenda_item import AgendaItem
from voteit.core.models.proposal import Proposal


class SubscriberTests(TestCase):
    """ integration tests """

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_subscriber_adds(self):
        self.config.include('voteit.irl')
        ai = AgendaItem()
        prop = ai['p'] = Proposal()
        self.assertEqual(prop.get_field_value('proposal_number', object()), 1)
