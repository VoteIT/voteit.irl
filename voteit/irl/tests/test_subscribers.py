from unittest import TestCase

from pyramid import testing
from voteit.core.models.user import User
from voteit.core.models.meeting import Meeting
from voteit.core.security import ROLE_VIEWER
from voteit.core.security import ROLE_VOTER
from voteit.core.testing_helpers import bootstrap_and_fixture
from voteit.core.testing_helpers import register_security_policies

from voteit.irl.models.electoral_register import ElectoralRegister
from voteit.irl.models.eligible_voters import EligibleVoters


ALL_TEST_USERS = set(('fredrik', 'anders', 'hanna', 'robin', 'admin'))
SOME_TEST_USERS = set(('fredrik', 'anders', 'hanna'))
SOME_OTHER_TEST_USERS = set(('fredrik', 'robin'))


class SubscriberTests(TestCase):
    """ integration tests """

    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        self.m = Meeting()

    def tearDown(self):
        testing.tearDown()

    def test_update_eligible_voters(self):
        register_security_policies(self.config)
        root = bootstrap_and_fixture(self.config)
        
        for userid in ALL_TEST_USERS-set(('admin',)):
            root.users[userid] = User()

        root['m'] = self.m
        
        self.config.include('voteit.irl')
        
        # give some users ROLE_VIEWER, ROLE_VOTER in the meeting
        security = []
        for userid in SOME_TEST_USERS:
            security.append({'userid': userid, 'groups': (ROLE_VIEWER, ROLE_VOTER,)}) 
        self.m.set_security(security)
        
        # check that eligible voters is correct
        eligible_voters = EligibleVoters(self.m)
        for userid in SOME_TEST_USERS:
            self.assertIn(userid, eligible_voters.list)
        
        # check that no user without ROLE_VOTER is in list
        for userid in ALL_TEST_USERS-SOME_TEST_USERS:
            self.assertNotIn(userid, eligible_voters.list)

    def test_update_electoral_register(self):
        register_security_policies(self.config)
        root = bootstrap_and_fixture(self.config)
        
        for userid in ALL_TEST_USERS-set(('admin',)):
            root.users[userid] = User()

        root['m'] = self.m
        
        self.config.include('voteit.irl')
        
        # give some users ROLE_VIEWER, ROLE_VOTER in the meeting
        security = []
        for userid in SOME_TEST_USERS:
            security.append({'userid': userid, 'groups': (ROLE_VIEWER, ROLE_VOTER,)}) 
        self.m.set_security(security)

        # check that a new electoral register has been archived
        electoral_register = ElectoralRegister(self.m)
        self.assertEqual(len(electoral_register.archive), 1)
        
        self.assertEqual(len(electoral_register.archive['1']['userids']), 3)
        self.assertIn('fredrik', electoral_register.archive['1']['userids'])
        self.assertIn('anders', electoral_register.archive['1']['userids'])
        self.assertIn('hanna', electoral_register.archive['1']['userids'])
        self.assertNotIn('robin', electoral_register.archive['1']['userids'])
        
        # give some users other users ROLE_VIEWER, ROLE_VOTER in the meeting
        security = []
        for userid in SOME_OTHER_TEST_USERS:
            security.append({'userid': userid, 'groups': (ROLE_VIEWER, ROLE_VOTER,)}) 
        self.m.set_security(security)
        
        self.assertEqual(len(electoral_register.archive), 2)
        
        self.assertEqual(len(electoral_register.archive['2']['userids']), 2)
        self.assertIn('fredrik', electoral_register.archive['2']['userids'])
        self.assertIn('robin', electoral_register.archive['2']['userids'])
        self.assertNotIn('anders', electoral_register.archive['2']['userids'])
        self.assertNotIn('hanna', electoral_register.archive['2']['userids'])