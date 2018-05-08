
def includeme(config):
    config.include('.change_owner')
    config.include('.electoral_register')
    config.include('.eligible_voters')
    config.include('.meeting_presence')
    config.include('.participant_callbacks')
    config.include('.participant_numbers')
    config.include('.print')
    config.include('.projector')
    config.include('.proposals_unhandled')
    config.include('.main_proposals')
