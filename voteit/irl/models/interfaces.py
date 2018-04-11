from zope.interface import Interface
from zope.interface import Attribute


class IMeetingPresence(Interface):
    """ Utility to check who's present. It only stores users in memory during check,
        but other systems might store and use the information.
    """
    open = Attribute("Is the process currently open? True or False.")
    present_userids = Attribute("Set of present userids, volatile storage")
    start_time = Attribute("Time when the check was started, or None")
    archive = Attribute("Storage for previous checks")
    enabled = Attribute("Is this tool enabled for this meeting?")
    vote_transfer_enabled = Attribute("Is vote transfers enabled for this meeting?")

    def __init__(context):
        """ Context to adapt """

    def start_check():
        """ Start or enable the check for user presence. """

    def end_check():
        """ End the check. """

    def add(userid):
        """ Add a userid. Only works when the check is open. """

    def remove(userid):
        """ Remove a userid. Only works when the check is open. """

    def archive_current():
        """ Archive and timestamp the current check."""


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


class IParticipantNumbers(Interface):
    """ An adapter that handles numbering of meeting participants.
    """
    tickets = Attribute("Storage for tickets")
    userid_to_number = Attribute("Map userid -> number")
    number_to_userid = Attribute("Map number -> userid")
    token_to_number = Attribute("Map token -> number - good for validation too.")
    email_to_number = Attribute("Map email -> number")

    def __init__(context):
        """ context is always meeting. """

    def new_tickets(creator, start, end = None):
        """ Create new tickets between start number to end number.
            Returns a generator of all created numbers.
            Note that this method won't overwrite any previously created numbers,
            it will simply fill the gaps.

            creator
                UserID of the person who created this ticket.

            start
                Number to start at

            end
                Number to end at. No arg means just do one number.
        """

    def claim_ticket(userid, token):
        """ Claim a ticket for userid.
        """

    def clear_numbers(start, end = None):
        """ Clear a range of numbers.
            Removes all data including any registered tickets.
            Method won't raise exceptions if number doesn't exist.
            Returns a generator of cleared numbers.

            start
                Which number to start at

            end
                Number to end at. No arg means just do one number.
        """

    def clear_number(number):
        """ Remove all data for this number. This includes any registered tickets etc.
            Will return cleared number if anything was cleared.
        """

    def attach_email(email, number):
        """ Attach an email address to this number.
        """


class IParticipantCallbacks(Interface):
    """ Stores participant callbacks to be performed when a user claims a participant number.
    """

    def __init__(context):
        """ Always adapts meetings. """

    def get_callbacks(number):
        """ Return a list of callback names for a specific number. """

    def execute_callbacks_for(number, userid, limit = None, request = None):
        """ Execute all associated callbacks for the user associated with the number.
            Will add a flash message to the request if something wasn't able to run.

            number
                This is the number you want to execute for.

            userid
                Of the user that the number is associated with.

            limit (list or string)
                Only execute callbacks with this name(s).

            request
                Will be fetched if it's none.
        """

    def add(callback, start, end = None):
        """ Add a new callback.

            callback
                Name of the IParticipantCallback adapter to execute.

            start
                Integer number to start at.

            end
                Integer number to stop at, or None if you just want to add one number.
        """

    def remove(callback, start, end = None):
        """ Remove a  callback. Note that callbacks already run will already have taken effect.
            It doesn't undo this!

            callback
                Name of the IParticipantCallback adapter to remove.

            start
                Integer number to start at.

            end
                Integer number to stop at, or None if you just want to add one number.
        """


class IParticipantCallback(Interface):
    """ A special adapter that performs actions when someone claims a participant number,
        or for users that have already claimed one.
    """
    name = Attribute("Name of this adapter. Must be unique.")
    title = Attribute("Readable title.")
    description = Attribute("Optional description of this callback.")
    
    def __init__(context):
        """ Always adapts meetings. """

    def __call__(number, userid, **kw):
        """ Perform action on meeting conserning this number and userid. """
