from copy import deepcopy

from pyramid.events import subscriber
from pyramid.threadlocal import get_current_request
from pyramid.traversal import find_interface
from repoze.folder.interfaces import IObjectAddedEvent
from zope.component import getAdapter

from voteit.core.interfaces import IObjectUpdatedEvent
from voteit.core.models.interfaces import IAgendaItem, IMeeting, IProposal
from voteit.core.security import ROLE_VOTER
from voteit.core.security import find_authorized_userids

from voteit.irl.models.interfaces import IElectoralRegister
from voteit.irl.models.interfaces import IEligibleVoters 
from voteit.irl.models.interfaces import IProposalNumbers

from pyramid.security import has_permission


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
    
    voters = set()
    for item in obj.get_security():
        if ROLE_VOTER in item['groups']:
            voters.add(item['userid'])
        
    eligible_voters.list.update(voters)
    

@subscriber([IMeeting, IObjectUpdatedEvent])
def update_electoral_register(obj, event):
    request = get_current_request()
    electoral_register = request.registry.getAdapter(obj, IElectoralRegister)
    
    voters = set()
    for item in obj.get_security():
        if ROLE_VOTER in item['groups']:
            voters.add(item['userid'])
            
    last = None    
    if electoral_register.archive.keys():
        last = max(electoral_register.archive.keys())

    if not last or voters != electoral_register.archive[last]:
        electoral_register.add_archive(voters)