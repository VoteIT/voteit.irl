#from unittest import TestCase
#
#from pyramid import testing
#
#from voteit.core.testing_helpers import bootstrap_and_fixture
#from voteit.core.models.interfaces import IMeeting
#
#from voteit.irl.models.interfaces import IElectoralRegister
#from voteit.irl.models.interfaces import IEligibleVoters
#from voteit.irl.models.electoral_register import ElectoralRegister
#from voteit.irl.models.eligible_voters import EligibleVoters
#
#

#FIXME: These tests are based on the old views - update


#class ViewTests(TestCase):
#    """ integration tests """
#
#    def setUp(self):
#        self.request = testing.DummyRequest()
#        self.config = testing.setUp(request=self.request)
#
#    def tearDown(self):
#        testing.tearDown()
#        
#    @property
#    def _cut(self):
#        from voteit.irl.views.electoral_register import ElectoralRegisterView
#        return ElectoralRegisterView
#    
#    def _fixture(self):
#        settings = self.config.registry.settings
#        settings['default_locale_name'] = 'sv'
#        settings['default_timezone_name'] = 'Europe/Stockholm'
#        self.config.include('voteit.core.models.date_time_util')
#        
#        root = bootstrap_and_fixture(self.config)
#
#        from voteit.core.models.user import User
#        for userid in ('fredrik', 'anders', 'hanna', 'robin'):
#            root.users[userid] = User()
#        
#        from voteit.core.models.meeting import Meeting
#        root['m'] = meeting = Meeting()
#    
#        self.config.registry.registerAdapter(EligibleVoters, (IMeeting,), IEligibleVoters)
#        
#        eligible_voters = self.request.registry.getAdapter(meeting, IEligibleVoters)
#        eligible_voters.list.update(('fredrik', 'anders', 'hanna', 'robin'))
#        
#        self.config.registry.registerAdapter(ElectoralRegister, (IMeeting,), IElectoralRegister)
#        
#        return meeting
#
#    def test_view(self):
#        context = self._fixture()
#        
#        register = self.request.registry.getAdapter(context, IElectoralRegister)
#        register.register.update(('fredrik', 'anders', 'hanna', 'admin'))
#        register.close()
#        
#        obj = self._cut(context, self.request)
#        
#        result = obj.view()
#        
#        self.assertIn('archive', result)
#        self.assertIn('register', result)
#        
#    def test_diff_electoral_register(self):
#        context = self._fixture()
#        
#        register = self.request.registry.getAdapter(context, IElectoralRegister)
#        register.register.update(('fredrik', 'anders'))
#        register.close()
#        
#        register.register.update(('fredrik', 'hanna', 'robin'))
#        register.close()
#        
#        self.request.POST = {'view': 'view', 'archive1': '1', 'archive2': '2'}
#        obj = self._cut(context, self.request)
#        result = obj.diff_electoral_register()
#        
#        self.assertEqual(result['archive1'], register.archive['1'])
#        self.assertEqual(result['archive2'], register.archive['2'])
#        self.assertEqual(result['union'], set(['anders', 'hanna', 'fredrik', 'robin']))