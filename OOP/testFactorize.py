import unittest


def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ['string',  1.5]
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = [-1,  -10,  -100]
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = [0, 1]
        with self.subTest(case=0):
            self.assertEqual(factorize(0), (0,))
        with self.subTest(case=1):
            self.assertEqual(factorize(1), (1,))

    def test_simple_numbers(self):
        cases = [3, 13, 29]
        for x in cases:
            with self.subTest(case=x):
                self.assertEqual(factorize(x), (x,))

    def test_two_simple_multipliers(self):
        cases = [6, 26, 121]
        with self.subTest(case=6):
            self.assertEqual(factorize(6), (2, 3))
        with self.subTest(case=26):
            self.assertEqual(factorize(26), (2, 13))
        with self.subTest(case=121):
            self.assertEqual(factorize(121), (11, 11))

    def test_many_multipliers(self):
        cases = [1001, 9699690]
        with self.subTest(case=1001):
            self.assertEqual(factorize(1001), (7, 11, 13))
        with self.subTest(case=9699690):
            self.assertEqual(factorize(9699690), (2, 3, 5, 7, 11, 13, 17, 19))


if __name__ == '__main__':
    unittest.main()