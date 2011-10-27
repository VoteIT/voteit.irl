

def includeme(config):
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('vote.irl', 'vote.irl:static', cache_max_age = cache_ttl_seconds)
    config.scan('voteit.irl')
