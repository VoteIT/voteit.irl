

def includeme(config):
    """ Include required components. You can include this by simply adding voteit.irl
        to the section "plugins" in your paster .ini file.
    """
    from voteit.core.models.interfaces import IAgendaItem
    from voteit.irl.models.proposal_numbers import ProposalNumbers
    from voteit.irl.interfaces import IProposalNumbers
    config.registry.registerAdapter(ProposalNumbers, required = (IAgendaItem,), provided = IProposalNumbers)
    
    config.scan('voteit.irl')
