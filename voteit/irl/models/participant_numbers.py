from random import choice

from BTrees.IOBTree import IOBTree
from BTrees.OIBTree import OIBTree
from arche.utils import utcnow
from persistent import Persistent
from pyramid.threadlocal import get_current_registry
from voteit.core.models.interfaces import IMeeting
from zope.component import adapter
from zope.interface import implementer
from pyramid.traversal import find_root
from arche.interfaces import IEmailValidatedEvent
from pyramid.traversal import find_resource
from pyramid.threadlocal import get_current_request

from voteit.irl.models.interfaces import IParticipantNumbers
from voteit.irl.events import ParticipantNumberClaimed


CHAR_POOL = u"23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"


@implementer(IParticipantNumbers)
@adapter(IMeeting)
class ParticipantNumbers(object):

    def __init__(self, context):
        self.context = context

    @property
    def tickets(self):
        try:
            return self.context.__participant_numbers_tickets__
        except AttributeError:
            self.context.__participant_numbers_tickets__ = IOBTree()
            return self.context.__participant_numbers_tickets__

    @property
    def userid_to_number(self):
        try:
            return self.context.__participant_numbers_userid_to_number__
        except AttributeError:
            self.context.__participant_numbers_userid_to_number__ = OIBTree()
            return self.context.__participant_numbers_userid_to_number__

    @property
    def number_to_userid(self):
        try:
            return self.context.__participant_numbers_number_to_userid__
        except AttributeError:
            self.context.__participant_numbers_number_to_userid__ = IOBTree()
            return self.context.__participant_numbers_number_to_userid__

    @property
    def token_to_number(self):
        try:
            return self.context.__participant_numbers_token_to_number__
        except AttributeError:
            self.context.__participant_numbers_token_to_number__ = OIBTree()
            return self.context.__participant_numbers_token_to_number__

    @property
    def email_to_number(self):
        try:
            return self.context.__participant_numbers_email_to_number__
        except AttributeError:
            self.context.__participant_numbers_email_to_number__ = OIBTree()
            return self.context.__participant_numbers_email_to_number__

    def next_free(self):
        try:
            return self.tickets.maxKey() + 1
        except ValueError:
            return 1

    def new_token(self):
        def _token_part():
            return "".join([choice(CHAR_POOL) for x in range(choice(range(4, 5)))])
        token = None
        i = 0
        while token is None or token in self.token_to_number:
            token = u"%s-%s" % (_token_part(), _token_part())
            i += 1
            if i > 200:
                raise ValueError("Can't find any free token number. This should never happen.") #pragma : no cover
        return token

    def new_tickets(self, creator, start, end = None):
        if end == None:
            end = start
        assert start <= end
        results = []
        for i in range(start, end + 1): #Range  stops before end otherwise
            if i in self.tickets:
                continue
            token = self.new_token()
            ticket = ParticipantNumberTicket(i, token, creator)
            self.tickets[i] = ticket
            self.token_to_number[token] = i
            results.append(i)
        return results

    def claim_ticket(self, userid, token):
        number = self.token_to_number[token]
        self.tickets[number].claim(userid)
        self.number_to_userid[number] = userid
        self.userid_to_number[userid] = number
        reg = get_current_registry()
        reg.notify(ParticipantNumberClaimed(self.context, number, userid))
        return number

    def clear_number(self, number):
        userid = self.number_to_userid.get(number, None)
        if number in self.number_to_userid:
            del self.number_to_userid[number]
        if userid and userid in self.userid_to_number:
            del self.userid_to_number[userid]
        if number in self.tickets:
            ticket = self.tickets[number]
            if ticket.email and ticket.email in self.email_to_number:
                del self.email_to_number[ticket.email]
            token = ticket.token
            del self.tickets[number]
            del self.token_to_number[token]
            return number

    def clear_numbers(self, start, end = None):
        if end == None:
            end = start
        assert start <= end
        results = []
        for i in range(start, end + 1): #Range  stops before end otherwise
            if i in self.tickets:
                self.clear_number(i)
                results.append(i)
        return results

    def attach_email(self, email, number):
        ticket = self.tickets[number]
        ticket.email = email
        self.email_to_number[email] = number

    def __nonzero__(self):
        return True
    __bool__ = __nonzero__

    def __len__(self):
        return len(self.tickets)

    def __contains__(self, number):
        return number in self.tickets


class ParticipantNumberTicket(Persistent):
    number = None
    created = None
    claimed = None
    claimed_by = None
    token = None
    created_by = None
    email = None

    def __init__(self, number, token, creator):
        self.number = number
        self.created = utcnow()
        self.claimed = None
        self.claimed_by = None
        self.token = token
        self.created_by = creator

    def claim(self, userid):
        if self.claimed or self.claimed_by:
            raise TicketAlreadyClaimedError(u"Ticket already claimed")
        self.claimed = utcnow()
        self.claimed_by = userid


class TicketAlreadyClaimedError(Exception):
    """ Ticket has already been claimed by someone else. """


def auto_claim_pn_when_email_validated(event):
    #FIXME: Typical example of task that should be sent to a worker queue instead.
    #It hardly requires atomicity
    root = find_root(event.user)
    address_for_docid = root.document_map.address_for_docid
    query = "type_name == 'Meeting' and "
    query += "workflow_state in any(['ongoing', 'upcoming'])"
    request = get_current_request()
    for docid in root.catalog.query(query)[1]:
        path = address_for_docid(docid)
        meeting = find_resource(root, path)
        pns = IParticipantNumbers(meeting)
        if event.user.email in pns.email_to_number:
            number = pns.email_to_number[event.user.email]
            ticket = pns.tickets[number]
            if ticket.claimed == None:
                pns.claim_ticket(event.user.userid, ticket.token)

def includeme(config):
    config.registry.registerAdapter(ParticipantNumbers)
    config.add_subscriber(auto_claim_pn_when_email_validated, IEmailValidatedEvent)
