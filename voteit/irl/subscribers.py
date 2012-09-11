from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from repoze.folder.interfaces import IObjectAddedEvent
from pyramid.events import subscriber
from pyramid.traversal import find_interface
from zope.component import getAdapter

from voteit.irl.models.interfaces import IProposalNumbers


@subscriber([IProposal, IObjectAddedEvent])
def add_proposal_number(obj, event):
    """ Add a number to a new Proposal.
    """
    ai = find_interface(obj, IAgendaItem)
    numbers = getAdapter(ai, IProposalNumbers)
    numbers.add(obj)
