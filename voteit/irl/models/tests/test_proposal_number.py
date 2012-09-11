from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from voteit.core.models.agenda_item import AgendaItem
from voteit.core.models.proposal import Proposal

from voteit.irl.models.interfaces import IProposalNumbers


class ProposalNumberTests(TestCase):
    """ unit tests """

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from voteit.irl.models.proposal_numbers import ProposalNumbers
        return ProposalNumbers

    def test_verify_class(self):
        self.failUnless(verifyClass(IProposalNumbers, self._fut))

    def test_verify_obj(self):
        context = testing.DummyModel()
        self.failUnless(verifyObject(IProposalNumbers, self._fut(context)))

    def test_adapter_registered_on_include(self):
        self.config.include('voteit.irl')
        ai = AgendaItem()
        self.failUnless(self.config.registry.queryAdapter(ai, IProposalNumbers))

    def test_add(self):
        ai = AgendaItem()
        prop = ai['p'] = Proposal()
        obj = self._fut(ai)
        obj.add(prop)
        self.assertEqual(prop.get_field_value('proposal_number', object()), 1)
        self.failUnless(1 in obj.propnums)
        
        prop2 = ai['p2'] = Proposal()
        obj.add(prop2)
        self.assertEqual(prop2.get_field_value('proposal_number', object()), 2)
        self.failUnless(2 in obj.propnums)
