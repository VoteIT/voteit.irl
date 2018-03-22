# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass
from voteit.core.models.meeting import Meeting


class GenderTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from voteit.irl.plugins.gender import GenderStatistics
        return GenderStatistics

    def test_percentages(self):
        stats = self._cut()
        stats.add('female', 1)
        stats.add('male', 3)
        stats.add('', 1)
        self.assertEqual(stats.results, {
            'female': 1,
            'male': 3,
            'other': 0,
            '': 1,
        })
        self.assertEqual(stats.total, 5)
        sums = stats.sums
        expected = {
            'female': 20,
            'male': 60,
            'other': 0,
            '': 20,
        }
        for sum in sums:
            self.assertEqual(expected[sum.gender], sum.percentage)
