from zope.interface import Interface
from zope.interface import Attribute


class IMeetingPresence(Interface):
    """ Utility to check who's present. It only stores users in memory during check,
        but other systems might store and use the information.
    """
    open = Attribute("Is the process currently open? True or False.")
    present_userids = Attribute("Set of present userids")
    start_time = Attribute("Time when the check was started, or None")
    end_time = Attribute("Time when the check ended, or None")

    def __init__(context):
        """ Context to adapt """

    def start_check():
        """ Start or enable the check for user presence. """

    def end_check():
        """ End the check. """

    def add(userid):
        """ Add a userid. Only works when the check is open. """


class IElectoralRegister(Interface):
    """ Create an electoral register from the currently set voters.
        Adapter that adapts IMeeting.
    """
    registers = Attribute("Stored registers.")
    current = Attribute("Currently active register, IE the last one.")

    def __init__(context):
        """ Context to adapt, which must be meeting"""

    def get_next_key():
        """" Get next free key for register. """

    def currently_set_voters():
        """ Get a frozenset of userids who have the voter role currently.
        """

    def new_register(userids):
        """ Create a new register from a list-like item of userids. """

    def new_register_needed():
        """ Return a bool of wether a new register is needed. """


class IElegibleVotersMethod(Interface):
    """ An adapter that will figure out who should be voter and who shouldn't.
    """
    name = Attribute("Name or ID of the adapter. Should be used when registering it.")
    title = Attribute("Readable title")
    description = Attribute("Description of this method")

    def __init__(context):
        """ context to adapt, which should always be a meeting. """

    def get_voters(**kw):
        """ Return an iterable with userids of everyone who should be able to vote.
        """
