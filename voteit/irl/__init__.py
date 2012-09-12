from pyramid.i18n import TranslationStringFactory

VoteIT_IRL_MF = TranslationStringFactory('voteit.irl')



def includeme(config):
    """ Include required components. You can include this by simply adding voteit.irl
        to the section "plugins" in your paster .ini file.
    """
    from voteit.core.models.interfaces import IAgendaItem
    from voteit.irl.models.proposal_numbers import ProposalNumbers
    from voteit.irl.models.interfaces import IProposalNumbers
    config.registry.registerAdapter(ProposalNumbers, required = (IAgendaItem,), provided = IProposalNumbers)
    
    from voteit.core.models.interfaces import IMeeting
    from voteit.irl.models.electoral_register import ElectoralRegister
    from voteit.irl.models.interfaces import IElectoralRegister
    config.registry.registerAdapter(ElectoralRegister, (IMeeting,), IElectoralRegister)
    
    from voteit.irl.models.delegates import Delegates
    from voteit.irl.models.interfaces import IDelegates
    config.registry.registerAdapter(Delegates, (IMeeting,), IDelegates)

    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('voteit_irl', 'voteit.irl:static', cache_max_age = cache_ttl_seconds)

    config.add_translation_dirs('voteit.irl:locale/')

    config.scan('voteit.irl')
