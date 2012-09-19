from voteit.core.models.interfaces import IMeeting
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from repoze.folder.interfaces import IObjectAddedEvent
from pyramid.events import subscriber
from pyramid.traversal import find_interface
from zope.component import getAdapter
from voteit.core.interfaces import IObjectUpdatedEvent
from voteit.core.security import ROLE_VOTER
from pyramid.threadlocal import get_current_request

from voteit.irl.models.interfaces import IEligibleVoters
from voteit.irl.models.interfaces import IProposalNumbers


@subscriber([IProposal, IObjectAddedEvent])
def add_proposal_number(obj, event):
    """ Add a number to a new Proposal.
    """
    ai = find_interface(obj, IAgendaItem)
    numbers = getAdapter(ai, IProposalNumbers)
    numbers.add(obj)


@subscriber([IMeeting, IObjectUpdatedEvent])
def update_eligible_voters(obj, event):
    request = get_current_request()
    eligible_voters = request.registry.getAdapter(obj, IEligibleVoters)
    for userid in find_authorized_userids(obj, (ROLE_VOTER, )):
        eligible_voters.list.add(userid)