from six import string_types
from voteit.core.security import ROLE_OWNER


def change_ownership(obj, userid):
    """ Change ownership of an object to another user.
        Will return the supplied userid if anything was changed.
    """
    assert isinstance(userid, string_types)
    old_owner = obj.creators[0]
    if userid == old_owner:
        return
    #Remove Owner group from old owner
    obj.local_roles.remove(old_owner, ROLE_OWNER)
    #Add new owner
    obj.local_roles.add(userid, ROLE_OWNER)
    #Set new owner in creators attr - this will also trigger reindex catalog event so keep it last!
    obj.set_field_appstruct({'creators': (userid,)})
    return userid
