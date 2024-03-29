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
        self.assertEqual(args.add, .7)
        self.assertIsNone(args.addlist)

        args = dispense_change.get_args("--addlist [.7]".split())
        self.assertEqual(args.addlist, '[.7]')
        self.assertIsNone(args.add)

        args = dispense_change.get_args("--addlist [.7,'g']".split())
        self.assertEqual(args.addlist, "[.7,'g']")
        self.assertIsNone(args.add)

        args = dispense_change.get_args("--addlist [.7,'g'] --add .3".split())
        self.assertEqual(args.addlist, "[.7,'g']")
        self.assertEqual(args.add, .3)

    def test_extend_coins(self):
        
        # testing add
        args = dispense_change.get_args("--add .7".split())

        coins = self.coins.copy()
        coins = dispense_change.extend_coins(coins, args)
        totals = dispense_change.dispense_coins(5.47, coins)
        self.assertEqual(totals[coins[0]], 7)
        self.assertEqual(totals[coins[1]], 2)
        self.assertEqual(totals[coins[2]], 0)
        self.assertEqual(totals[coins[3]], 1)
        self.assertEqual(totals[coins[4]], 2)

        # Testing addlist
        args = dispense_change.get_args("--addlist [.7]".split())

        coins = self.coins.copy()
        coins = dispense_change.extend_coins(coins, args)
        totals = dispense_change.dispense_coins(5.47, coins)
        self.assertEqual(totals[coins[0]], 7)
        self.assertEqual(totals[coins[1]], 2)
        self.assertEqual(totals[coins[2]], 0)
        self.assertEqual(totals[coins[3]], 1)
        self.assertEqual(totals[coins[4]], 2)

        # Testing addlist with add
        args = dispense_change.get_args("--addlist [.7] --add .3".split())

        coins = self.coins.copy()
        coins = dispense_change.extend_coins(coins, args)
        totals = dispense_change.dispense_coins(5.47, coins)
        # [.7, .3, .25, .10, .05, .01]
        self.assertEqual(totals[coins[0]], 7)
        self.assertEqual(totals[coins[1]], 1)
        self.assertEqual(totals[coins[2]], 1)
        self.assertEqual(totals[coins[3]], 0)
        self.assertEqual(totals[coins[4]], 0)
        self.assertEqual(totals[coins[5]], 2)

        # testing addlist with invalid input
        args = dispense_change.get_args("--addlist [.7,'g']".split())

        coins = self.coins.copy()
        coins = dispense_change.extend_coins(coins, args)
        totals = dispense_change.dispense_coins(5.47, coins)
        self.assertEqual(totals[coins[0]], 7)
        self.assertEqual(totals[coins[1]], 2)
        self.assertEqual(totals[coins[2]], 0)
        self.assertEqual(totals[coins[3]], 1)
        self.assertEqual(totals[coins[4]], 2)


if __name__ == "__main__":
    unittest.main()
