from zope.interface import Attribute
from zope.interface import Interface


class IParticipantNumberClaimed(Interface):
    """ Event that fires when a participant number is claimed by someone. """
    meeting = Attribute("Meeting object where the number was claimed")
    number = Attribute("Number claimed")
    userid = Attribute("UserID who claimed a number")
