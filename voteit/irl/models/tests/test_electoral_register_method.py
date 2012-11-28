#import unittest
#
#from pyramid import testing
#from zope.interface.verify import verifyObject
#
#from voteit.core.security import ROLE_VOTER
#
#
#ALL_TEST_USERS = set(('fredrik', 'anders', 'hanna', 'robin', 'admin'))
#VOTERS = set(('fredrik', 'anders', 'hanna'))
#
#class ElectoralRegisterMethodTests(unittest.TestCase):
#    def setUp(self):
#        self.config = testing.setUp()
#
#    def tearDown(self):
#        testing.tearDown()
#
#    def _make_adapted_obj(self):
#        from voteit.irl.models.electoral_register_method import ElectoralRegisterMethod
#        from voteit.core.models.meeting import Meeting
#        self.meeting = Meeting()
#        return ElectoralRegisterMethod(self.meeting)
#
#    def test_interface(self):
#        from voteit.irl.models.interfaces import IElectoralRegisterMethod
#        obj = self._make_adapted_obj()
#        self.assertTrue(verifyObject(IElectoralRegisterMethod, obj))
#
#    def test_apply(self):
#        obj = self._make_adapted_obj()
#
#        for userid in ALL_TEST_USERS:
#            self.meeting.add_groups(userid, (ROLE_VOTER, ), event=False)
#        
#        obj.apply(VOTERS)
#        
#        self.assertIn(ROLE_VOTER, self.meeting.get_groups('fredrik'))
#        self.assertIn(ROLE_VOTER, self.meeting.get_groups('anders'))
#        self.assertIn(ROLE_VOTER, self.meeting.get_groups('hanna'))
#        
#        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('robin'))
#        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('admin'))
#        self.assertNotIn(ROLE_VOTER, self.meeting.get_groups('dummy'))
#                
