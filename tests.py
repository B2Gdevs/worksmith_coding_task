import unittest
from unittest import mock
import dispense_change
import ast


class TestDespense(unittest.TestCase):

    def setUp(self):
        self.coins = [.25, .10, .05, .01]

    def test_get_input(self):

        with mock.patch('builtins.input', return_value="1.45678"):
            self.assertEqual(dispense_change.get_input(), 1.45)

        with mock.patch('builtins.input', return_value="1.4"):
            self.assertEqual(dispense_change.get_input(), 1.4)
        
        with mock.patch('builtins.input', return_value="1"):
            self.assertEqual(dispense_change.get_input(), 1)

    def test_dispense_coins(self):
        coins = self.coins.copy()

        # test natural numbers
        for i in range(0, 5):
            totals = dispense_change.dispense_coins(i, coins)
            self.assertEqual(totals[coins[0]], i//.25)
            self.assertEqual(totals[coins[1]], 0)
            self.assertEqual(totals[coins[2]], 0)
            self.assertEqual(totals[coins[3]], 0)

        # test real number
        totals = dispense_change.dispense_coins(5.47, coins)
        self.assertEqual(totals[coins[0]], 21)
        self.assertEqual(totals[coins[1]], 2)
        self.assertEqual(totals[coins[2]], 0)
        self.assertEqual(totals[coins[3]], 2)

        # test extended coins
        coins.append(.7)
        coins = sorted(coins, reverse=True)
        totals = dispense_change.dispense_coins(5.47, coins)
        self.assertEqual(totals[coins[0]], 7)
        self.assertEqual(totals[coins[1]], 2)
        self.assertEqual(totals[coins[2]], 0)
        self.assertEqual(totals[coins[3]], 1)
        self.assertEqual(totals[coins[4]], 2)

    def test_get_args(self):
        
        args = dispense_change.get_args("--add .7".split())

        coins = self.coins.copy()
        coins.append(args.add)
        coins = sorted(coins, reverse=True)
        totals = dispense_change.dispense_coins(5.47, coins)
        self.assertEqual(totals[coins[0]], 7)
        self.assertEqual(totals[coins[1]], 2)
        self.assertEqual(totals[coins[2]], 0)
        self.assertEqual(totals[coins[3]], 1)
        self.assertEqual(totals[coins[4]], 2)

        args = dispense_change.get_args("--addlist [.7]".split())

        coins = self.coins.copy()
        coins.extend(ast.literal_eval(args.addlist))
        coins = sorted(coins, reverse=True)
        totals = dispense_change.dispense_coins(5.47, coins)
        self.assertEqual(totals[coins[0]], 7)
        self.assertEqual(totals[coins[1]], 2)
        self.assertEqual(totals[coins[2]], 0)
        self.assertEqual(totals[coins[3]], 1)
        self.assertEqual(totals[coins[4]], 2)



if __name__ == "__main__":
    unittest.main()
