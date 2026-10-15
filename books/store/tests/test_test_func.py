from django.test import TestCase
from store.test_func import operations


class FuncTestCase(TestCase):
    def test_minus(self):
        r = operations(20, 5, '-')
        self.assertEqual(15, r)

    def test_multi(self):
        r = operations(10, 40, '*')
        self.assertEqual(400, r)