from __future__ import absolute_import
import unittest
import numpy as np

from ._example import EmptyCase


class TestBenchmarkCase(unittest.TestCase):
    def test_create_case(self):
        pass

    def test_set_up(self):
        """ Nothing should happen """
        EmptyCase(None).set_up()

    def test_tear_down(self):
        """ Nothing should happen """
        EmptyCase(None).tear_down()

    def test_set_up_class(self):
        """ Nothing should happen """
        def fake_set_up_class(clz):
            clz.data = np.zeros(10)
            clz.step = 10
            clz.rd = 1

        ec = EmptyCase(None)
        ec.set_up_class = fake_set_up_class.__get__(ec.__class__)
        ec.set_up_class()


    def test_run(self):
        """ Nothing should happen """
        def fake_set_up(obj):
            obj.data = np.zeros(10)
            obj.step = 10
            obj.rd = 1

        ec = EmptyCase(None)
        ec.set_up = fake_set_up.__get__(ec)
        ec.set_up()
