from zope.interface import Interface


class IProposalNumbers(Interface):
    """ Adapts agenda items to create proposal numbering.
        Makes sure each number is only used once.
    """

    def add(proposal):
        """ Add numbering to this proposal. Will also add proposals uid to
            record stored on adapted agenda item.
            The agenda items record isn't displayed anywhere currently.
        """
