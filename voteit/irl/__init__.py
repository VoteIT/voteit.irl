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

    from voteit.irl.models.meeting_presence import MeetingPresence
    from voteit.irl.models.interfaces import IMeetingPresence
    config.registry.registerAdapter(MeetingPresence, (IMeeting,), IMeetingPresence)

    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('voteit_irl', 'voteit.irl:static', cache_max_age = cache_ttl_seconds)

    config.add_translation_dirs('voteit.irl:locale/')
    #Add translations used within javascript
    from voteit.core.models.interfaces import IJSUtil
    _ = VoteIT_IRL_MF
    js_trans = config.registry.queryUtility(IJSUtil)
    if js_trans:
        js_trans.add_translations(
            register_meeting_presence_error_notice = _(u"register_meeting_presence_error_notice",
                                                       default = u"VoteIT wasn't able to set you as present. This might be due to server load, "
                                                       u"please try again in a short while."),
        )
    #FIXME:Tests don't need to load js util but we want to have proper logging here
    config.scan('voteit.irl')
