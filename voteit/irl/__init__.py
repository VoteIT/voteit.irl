from pyramid.i18n import TranslationStringFactory

VoteIT_IRL_MF = TranslationStringFactory('voteit.irl')



def includeme(config):
    """ Include required components. You can include this by simply adding voteit.irl
        to the section "plugins" in your paster .ini file.
    """
    from voteit.core.models.interfaces import IMeeting
    from voteit.irl.models.electoral_register import ElectoralRegister
    from voteit.irl.models.interfaces import IElectoralRegister
    config.registry.registerAdapter(ElectoralRegister, (IMeeting,), IElectoralRegister)
    
    from voteit.irl.models.eligible_voters import EligibleVoters
    from voteit.irl.models.interfaces import IEligibleVoters
    config.registry.registerAdapter(EligibleVoters, (IMeeting,), IEligibleVoters)
    
    from voteit.irl.models.electoral_register_method import ElectoralRegisterMethod
    from voteit.irl.models.interfaces import IElectoralRegisterMethod
    config.registry.registerAdapter(ElectoralRegisterMethod, (IMeeting,), IElectoralRegisterMethod, ElectoralRegisterMethod.name)

    from voteit.irl.models.meeting_presence import MeetingPresence
    from voteit.irl.models.interfaces import IMeetingPresence
    config.registry.registerUtility(MeetingPresence(), IMeetingPresence)

    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('voteit_irl', 'voteit.irl:static', cache_max_age = cache_ttl_seconds)

    config.add_translation_dirs('voteit.irl:locale/')
    #Add translations used within javascript
    from voteit.core.models.interfaces import IJSUtil
    _ = VoteIT_IRL_MF
    js_trans = config.registry.getUtility(IJSUtil)
    js_trans.add_translations(
        register_meeting_presence_error_notice = _(u"register_meeting_presence_error_notice",
                                                   default = u"VoteIT wasn't able to set you as present. This might be due to server load, "
                                                   u"please try again in a short while."),
    )
    config.scan('voteit.irl')
