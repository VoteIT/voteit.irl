from zope.interface import Interface
from zope.interface import Attribute


class IProposalNumbers(Interface):
    """ Adapts agenda items to create proposal numbering.
        Makes sure each number is only used once.
    """

    def add(proposal):
        """ Add numbering to this proposal. Will also add proposals uid to
            record stored on adapted agenda item.
            The agenda items record isn't displayed anywhere currently.
        """


class IMeetingPresence(Interface):
    """ Utility to check who's present. It only stores users in memory during check,
        but other systems might store and use the information.
    """

    open = Attribute("Is the process currently open? True or False.")
    present_userids = Attribute("Set of present userids")
    start_time = Attribute("Time when the check was started, or None")
    end_time = Attribute("Time when the check ended, or None")

    def start_check():
        """ Start or enable the check for user presence. """

    def end_check():
        """ End the check. """

    def add(userid):
        """ Add a userid. Only works when the check is open. """


class IElectoralRegister(Interface):
    """ 
    """
    
    
class IEligibleVoters(Interface):
    """ 
    """
    
    
class IElectoralRegisterMethod(Interface):
    """
    """
    
    def apply(userids):
        """ Apply voteing rights to context, based on the list of userids
        """