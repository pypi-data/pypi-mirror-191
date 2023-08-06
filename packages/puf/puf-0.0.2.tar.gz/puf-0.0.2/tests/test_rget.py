import unittest
from puf.rget import rget, rget1


class TestRget(unittest.TestCase):
    def test_empty_keys(self):
        self.assertEqual(rget1('ok', ''), 'ok')

    def test_normal(self):
        data = [True, {'k': ['helo', 'world']}]
        self.assertEqual(rget1(data, '1.k.0'), 'helo')

    def test_abnormal(self):
        data = object()
        with self.assertRaises(AttributeError):
            rget(data, 'k')
