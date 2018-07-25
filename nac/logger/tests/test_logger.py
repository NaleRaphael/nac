from __future__ import absolute_import
from io import BytesIO
import unittest
import numpy as np

from nac.logger import (LogReader, LogWriter)


# Reference: numpy/lib/tests/test_io.py
class TestLogReader(unittest.TestCase):
    def setUp(self):
        self.reader = LogReader()

    def test_read_int(self):
        """
        Note
        ----
        data_length = np.array([0, 1])
        time_taken = np.array([[0, 0],
                               [1, 1]])
        ```
        data_length
        v
        0, 0, 0
        1, 1, 1
           ^  ^
           time_taken
        ```
        """
        c = BytesIO()
        c.write('0,0,0\n1,1,1')
        c.seek(0)
        x, y = self.reader.read(c, delimiter=',')
        np.testing.assert_equal(x, np.array([0, 1]))
        np.testing.assert_equal(y, np.array([[0, 0], [1, 1]]))

    def test_read_float(self):
        c = BytesIO()
        c.write('{0:{fmt}},{1:{fmt}},{2:{fmt}}\n{3:{fmt}},{4:{fmt}},{5:{fmt}}'.format(
                0, 0, 0, 1, 1, 1, fmt='.18e'))
        c.seek(0)
        x, y = self.reader.read(c, delimiter=',')
        np.testing.assert_equal(x, np.array([0, 1], dtype=float))
        np.testing.assert_equal(y, np.array([[0, 0], [1, 1]], dtype=float))


class TestLogWritter(unittest.TestCase):
    def setUp(self):
        self.writer = LogWriter()

    def test_write_int(self):
        a = np.array([[1, 2], [3, 4]], dtype=int)
        c = BytesIO()
        self.writer.write(c, a, delimiter=',', fmt='%d')
        c.seek(0)
        lines = c.readlines()
        self.assertEquals(lines, [b'1,2\n', b'3,4\n'])


    def test_write_float(self):
        a = np.array([[1, 2], [3, 4]], dtype=float)
        c = BytesIO()
        self.writer.write(c, a, delimiter=',', fmt='%.18e')
        c.seek(0)
        lines = c.readlines()
        self.assertEquals(lines, 
                          [b'{:{fmt}},{:{fmt}}\n'.format(1, 2, fmt='.18e'),
                          b'{:{fmt}},{:{fmt}}\n'.format(3, 4, fmt='.18e')])
