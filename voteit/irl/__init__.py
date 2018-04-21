import logging

from pyramid.i18n import TranslationStringFactory

VoteIT_IRL_MF = _ = TranslationStringFactory('voteit.irl')

log = logging.getLogger(__name__)


def includeme(config):
    """ Include required components. You can include this by simply adding voteit.irl
        to the section "plugins" in your paster .ini file.
    """
    config.include('.models')
    config.include('.schemas')
    config.include('.views')
    config.include('.fanstaticlib')
    cache_max_age = int(config.registry.settings.get('arche.cache_max_age', 60*60*24))
    config.add_static_view('voteit_irl', 'voteit.irl:static', cache_max_age = cache_max_age)
    config.add_translation_dirs('voteit.irl:locale/')
