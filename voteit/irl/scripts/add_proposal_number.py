import csv
import transaction
import sys

from zope.component import getAdapter
from pyramid.traversal import resource_path

from voteit.core.models.catalog import metadata_for_query
from voteit.core.models.interfaces import IAgendaItem
from voteit.core.models.interfaces import IProposal
from voteit.core.scripts.worker import ScriptWorker
from voteit.irl.interfaces import IProposalNumbers


def add_proposal_number(*args):
    meetingname = sys.argv[1]
    
    worker = ScriptWorker('add_proposal_number')
    
    print "Add proposal number"
    root = worker.root
    meeting = worker.root[meetingname]

    try:
        # get all agenda items
        for ai in meeting.values():
            if IAgendaItem.providedBy(ai):
                print ai
                # loop proposals
                proposals = ai.get_content(iface=IProposal, sort_on = 'created',)
                for proposal in proposals:
                    if IProposal.providedBy(proposal):
                        print proposal
                        # add number
                        numbers = getAdapter(ai, IProposalNumbers)
                        numbers.add(proposal)

        transaction.commit()
    except Exception, e:
        worker.logger.exception(e)
        transaction.abort()
    
    worker.shutdown()
