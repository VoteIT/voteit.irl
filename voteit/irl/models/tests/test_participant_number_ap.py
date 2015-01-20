import unittest

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.meeting import Meeting
from voteit.core.views.base_view import BaseView
from voteit.core import security

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
        schema = obj.schema()
        self.assertIsInstance(schema, colander.SchemaNode)

    def test_create_schema_changed_when_public_roles(self):
        view = _fixture(self.config)
        view.context.set_field_value('pn_ap_public_roles', (security.ROLE_VIEWER,))
        obj = self._cut(view.context)
        schema = obj.schema()
        self.assertEqual(schema['token'].missing, u"")

    def test_handle_success(self):
        view = _fixture(self.config)
        obj = self._cut(view.context)
        obj.handle_success(view, {'token': 'abc'})
        pn = self.config.registry.getAdapter(view.context, IParticipantNumbers)
        self.assertEqual(pn.number_to_userid[1], 'jane')

    def test_handle_success_with_claimed_roles(self):
        claimed_roles = set((security.ROLE_VIEWER, security.ROLE_DISCUSS))
        view = _fixture(self.config)
        view.context.set_field_value('pn_ap_claimed_roles', claimed_roles)
        obj = self._cut(view.context)
        obj.handle_success(view, {'token': 'abc'})
        self.assertEqual(set(view.context.get_groups('jane')), claimed_roles)

    def test_handle_success_with_public_roles(self):
        public_roles = set((security.ROLE_VIEWER, security.ROLE_DISCUSS))
        view = _fixture(self.config)
        view.context.set_field_value('pn_ap_public_roles', public_roles)
        obj = self._cut(view.context)
        obj.handle_success(view, {'token': ''})
        self.assertEqual(set(view.context.get_groups('jane')), public_roles)

    def test_config_schema(self):
        self.config.scan('voteit.irl.schemas')
        obj = self._cut(Meeting())
        schema = obj.config_schema() #API not needed
        self.assertIsInstance(schema, colander.SchemaNode)


def _fixture(config):
    config.testing_securitypolicy(userid = 'jane', permissive = True)
    config.include('voteit.core.models.flash_messages')
    config.include('voteit.core.models.fanstatic_resources')
    config.include('voteit.irl.models.participant_numbers')
    config.scan('voteit.irl.schemas')
    meeting = Meeting()
    request = testing.DummyRequest()
    
    view = BaseView(meeting, request)
    pn = config.registry.getAdapter(meeting, IParticipantNumbers)
    pn.new_tickets('c', 1)
    pn.tickets[1].token = 'abc'
    pn.token_to_number['abc'] = 1
    return view
