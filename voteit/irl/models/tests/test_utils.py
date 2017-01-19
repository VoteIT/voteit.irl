import unittest

from pyramid import testing


class ChangeOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.include('arche.testing')

    def tearDown(self):
        testing.tearDown()

    @property
    def _fut(self):
        from voteit.irl.models.utils import change_ownership
        return change_ownership

    def _mk_obj(self):
        from voteit.core.models.discussion_post import DiscussionPost
        return DiscussionPost(creators = ['jane_doe'])

    def test_new_ownership(self):
        obj = self._mk_obj()
        #Just to make sure
        self.assertIn('role:Owner', obj.local_roles['jane_doe'])
        #Real test
        result = self._fut(obj, 'john_doe')
        self.assertIn('role:Owner', obj.local_roles['john_doe'])
        self.assertNotIn('role:Owner', obj.local_roles.get('jane_doe', []))
        self.assertEqual(obj.creators[0], 'john_doe')
        self.assertEqual(result, 'john_doe')

    def test_old_owner_specified(self):
        obj = self._mk_obj()
        result = self._fut(obj, 'jane_doe')
        self.assertEqual(result, None)
        self.assertIn('role:Owner', obj.local_roles['jane_doe'])
