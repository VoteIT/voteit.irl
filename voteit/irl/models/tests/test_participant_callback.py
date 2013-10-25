import unittest

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.meeting import Meeting

from voteit.irl.models.interfaces import IParticipantCallback
from voteit.irl.models.interfaces import IParticipantCallbacks


class ParticipantCallbacksTests(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request = request)

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.participant_callback import ParticipantCallbacks
        return ParticipantCallbacks

    def test_verify_class(self):
        self.assertTrue(verifyClass(IParticipantCallbacks, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IParticipantCallbacks, self._cut(Meeting())))

    def test_integration(self):
        self.config.include('voteit.irl.models.participant_callback')
        self.failUnless(self.config.registry.queryAdapter(Meeting(), IParticipantCallbacks))

    def test_add(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        added, existed = obj.add('call', 1, 2)
        self.assertEqual(existed, [])
        self.assertEqual(added, [1, 2])
        self.assertEqual(len(obj.callbacks), 2)

    def test_add_one(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        added, existed = obj.add('call', 1)
        self.assertEqual(added, [1])
        self.assertEqual(len(obj.callbacks), 1)
        self.assertEqual(len(obj.callbacks[1]), 1)

    def test_add_with_existing(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        obj.add('call', 1, 2)
        added, existed = obj.add('call', 1, 5)
        self.assertEqual(existed, [1, 2])
        self.assertEqual(added, [3, 4, 5])
        self.assertEqual(len(obj.callbacks), 5)

    def test_add_another_callback(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        obj.add('call', 1)
        obj.add('caller', 1)
        self.assertEqual(len(obj.callbacks), 1)
        self.assertEqual(len(obj.callbacks[1]), 2)

    def test_remove(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        obj.add('call', 1, 2)
        removed, nonexistent = obj.remove('call', 1, 3)
        self.assertEqual(removed, [1, 2])
        self.assertEqual(nonexistent, [3])
        self.assertEqual(len(obj.callbacks), 3)
        self.assertEqual(len(obj.callbacks[1]), 0)
        self.assertEqual(len(obj.callbacks[2]), 0)
        self.assertEqual(len(obj.callbacks[3]), 0)

    def test_remove_one(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        obj.add('call', 1, 2)
        removed, nonexistent = obj.remove('call', 1)
        self.assertEqual(removed, [1])
        self.assertEqual(nonexistent, [])
        self.assertEqual(len(obj.callbacks), 2)
        self.assertEqual(len(obj.callbacks[1]), 0)
        self.assertEqual(len(obj.callbacks[2]), 1)

    def test_remove_another(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        obj.add('call', 1)
        obj.add('caller', 1)
        removed, nonexistent = obj.remove('call', 1)
        self.assertEqual(removed, [1])
        self.assertEqual(nonexistent, [])
        self.assertEqual(len(obj.callbacks), 1)
        self.assertEqual(len(obj.callbacks[1]), 1)

    def test_execute_callbacks_for(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        _register_dummy_callback(self.config)
        obj.add('dummy', 1)
        results = []
        obj.execute_callbacks_for(1, 'casper', results = results)
        self.failUnless(results)

    def test_execute_callbacks_for_none_registered(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        self.assertEqual(len(obj.execute_callbacks_for(1, 'casper')), 0)

    def test_execute_callbacks_for_with_bad_callbacks(self):
        self.config.include('voteit.core.models.flash_messages')
        meeting = Meeting()
        obj = self._cut(meeting)
        _register_dummy_callback(self.config)
        obj.add('404', 1)
        results = []
        obj.execute_callbacks_for(1, 'casper', results = results)
        self.failIf(results)

    def test_execute_callbacks_for_with_limit(self):
        meeting = Meeting()
        obj = self._cut(meeting)
        _register_dummy_callback(self.config)
        obj.add('dummy', 1)
        obj.add('dummy_2', 1)
        results = []
        obj.execute_callbacks_for(1, 'casper', limit = 'dummy', results = results)
        self.assertEqual(results, ['dummy'])


class ParticipantCallbackTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.participant_callback import ParticipantCallback
        return ParticipantCallback

    def test_verify_class(self):
        self.assertTrue(verifyClass(IParticipantCallback, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IParticipantCallback, self._cut(Meeting())))


class AssignVoterRoleTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.participant_callback import AssignVoterRole
        return AssignVoterRole

    def test_verify_class(self):
        self.assertTrue(verifyClass(IParticipantCallback, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IParticipantCallback, self._cut(Meeting())))

    def test_integration(self):
        self.config.include('voteit.irl.models.participant_callback')
        self.failUnless(self.config.registry.queryAdapter(Meeting(), IParticipantCallback, name = 'allow_vote'))


class AssignDiscussRoleTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.participant_callback import AssignDiscussionRole
        return AssignDiscussionRole

    def test_verify_class(self):
        self.assertTrue(verifyClass(IParticipantCallback, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IParticipantCallback, self._cut(Meeting())))

    def test_integration(self):
        self.config.include('voteit.irl.models.participant_callback')
        self.failUnless(self.config.registry.queryAdapter(Meeting(), IParticipantCallback, name = 'allow_discuss'))


class AssignProposeRoleTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.models.participant_callback import AssignProposeRole
        return AssignProposeRole

    def test_verify_class(self):
        self.assertTrue(verifyClass(IParticipantCallback, self._cut))

    def test_verify_object(self):
        self.assertTrue(verifyObject(IParticipantCallback, self._cut(Meeting())))

    def test_integration(self):
        self.config.include('voteit.irl.models.participant_callback')
        self.failUnless(self.config.registry.queryAdapter(Meeting(), IParticipantCallback, name = 'allow_propose'))


def _register_dummy_callback(config):
    from voteit.irl.models.participant_callback import ParticipantCallback
    
    class _DummyCallback(ParticipantCallback):
        name = u"dummy"
        title = u"Dummy for testing"
    
        def __call__(self, number, userid, **kw):
            kw['results'].append(self.name) #Pass this when executing to make testing easier
    
    config.registry.registerAdapter(_DummyCallback, name = _DummyCallback.name)
    config.registry.registerAdapter(_DummyCallback, name = 'dummy_2')
