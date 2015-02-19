import logging

from pyramid.i18n import TranslationStringFactory

VoteIT_IRL_MF = _ = TranslationStringFactory('voteit.irl')

log = logging.getLogger(__name__)


def includeme(config):
    """ Include required components. You can include this by simply adding voteit.irl
        to the section "plugins" in your paster .ini file.
    """
    config.include('voteit.irl.models.electoral_register')
    config.include('voteit.irl.models.meeting_presence')
    config.include('voteit.irl.models.participant_numbers')
    config.include('voteit.irl.models.participant_callback')
    config.include('voteit.irl.models.participant_number_ap')

    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('voteit_irl', 'voteit.irl:static', cache_max_age = cache_ttl_seconds)

    config.add_translation_dirs('voteit.irl:locale/')
    #Add translations used within javascript
    from voteit.core.models.interfaces import IJSUtil
    js_trans = config.registry.queryUtility(IJSUtil)
    if js_trans:
        js_trans.add_translations(
            register_meeting_presence_error_notice = _(u"register_meeting_presence_error_notice",
                                                       default = u"VoteIT wasn't able to set you as present. This might be due to server load, "
                                                       u"please try again in a short while."),
            presence_success_notice = _(u"Your precence is received"),
        )
    else:
        log.warn("No IJSUtil found so JS translations won't be loaded.")
    config.scan('voteit.irl')
