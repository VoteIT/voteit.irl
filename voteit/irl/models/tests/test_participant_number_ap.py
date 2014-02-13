import unittest

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.meeting import Meeting
from voteit.core.views.api import APIView

from voteit.core.models.interfaces import IAccessPolicy
from voteit.irl.models.interfaces import IParticipantNumbers
from voteit.irl.interfaces import IParticipantNumberClaimed


class ParticipantNumberAPTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.participant_number_ap import ParticipantNumberAP
        return ParticipantNumberAP

    def test_verify_class(self):
        self.assertTrue(verifyClass(IAccessPolicy, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IAccessPolicy, self._cut(Meeting())))

    def test_create_schema(self):
        self.config.scan('voteit.irl.schemas')
        obj = self._cut(Meeting())
        schema = obj.schema(None) #API not used
        self.assertIsInstance(schema, colander.SchemaNode)

    def test_handle_success(self):
        api = _fixture(self.config)
        obj = self._cut(api.meeting)
        obj.handle_success(api, {'token': 'abc'})
        pn = self.config.registry.getAdapter(api.meeting, IParticipantNumbers)
        self.assertEqual(pn.number_to_userid[1], 'jane')



def _fixture(config):
    config.testing_securitypolicy(userid = 'jane', permissive = True)
    config.include('voteit.core.models.flash_messages')
    config.include('voteit.irl.models.participant_numbers')
    meeting = Meeting()
    request = testing.DummyRequest()
    api = APIView(meeting, request)
    pn = config.registry.getAdapter(meeting, IParticipantNumbers)
    pn.new_tickets('c', 1)
    pn.tickets[1].token = 'abc'
    pn.token_to_number['abc'] = 1
    return api
    




#         participant_numbers = api.request.registry.getAdapter(api.meeting, IParticipantNumbers)
#         number = participant_numbers.claim_ticket(api.userid, appstruct['token'])
#         msg = _(u"number_now_assigned_notice",
#                 default = u"You're now assigned number ${number}.",
#                 mapping = {'number': number})
#         api.flash_messages.add(msg)
#         return HTTPFound(location = api.meeting_url)