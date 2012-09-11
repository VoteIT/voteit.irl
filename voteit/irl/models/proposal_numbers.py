from BTrees.IOBTree import IOBTree
from zope.component import adapts
from zope.interface.declarations import implements
from voteit.core.models.interfaces import IAgendaItem

from voteit.irl.models.interfaces import IProposalNumbers


class ProposalNumbers(object):
    """ See IProposalNumbers """
    implements(IProposalNumbers)
    adapts(IAgendaItem)

    def __init__(self, context):
        self.context = context
        try:
            self.propnums = self.context.__proposal_numbers__
        except AttributeError:
            self.propnums = self.context.__proposal_numbers__ = IOBTree()
            self.propnums[0] = u'' #Skip first key

    def add(self, proposal):
        number = self.propnums.maxKey() + 1
        proposal.set_field_value('proposal_number', number)
        self.propnums[number] = proposal.uid
