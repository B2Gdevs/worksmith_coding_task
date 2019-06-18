"""
Converts the numeric input in to counts of the coins used to make the input.

This script can take optional arguments such as add which allows one float 
value or a literal composite datatype such as a list or tuple.  Both types of 
input will extend the default coins in use which are .25, .10, .05, .01.

Author: Benjamin Garrard
Date: 6/17/2019
"""
from collections import defaultdict
import argparse
import ast
import sys


def get_input() -> float:
    """
    Gather user input and format it.

    Returns
    -------
    float:
        User input as a float if valid.

    """
    prec = 2

    # no error handling since float will throw an error if invalid.
    money_input = input("\nInput monetary amount: ").split('.')

    if len(money_input) < 2:
        return float(money_input[0])

    # truncate after decimal place to precision specified if decimal
    money_input = "{}.{:.{p}}".format(money_input[0], money_input[1], p=prec)
    money_input = float(money_input)
    return money_input


def dispense_coins(money_input: float, coins: list) -> defaultdict:
    """
    Convert input to count of coins.

    Parameters
    ----------
    money_input: float
        A float that has been processed by get_input.
    coins: list
        A list of coins that will be used to convert input to total
        of coins.

    Returns
    -------
    defaultdict:
        A dictionary that has the counts of each coin.

    """
    totals = defaultdict(lambda: 0)
    idx = 0

    while money_input > 0:
        if money_input < coins[idx]:
            idx += 1
            continue

        money_input = round((money_input - coins[idx]), 2)
        totals[coins[idx]] += 1

    return totals


def get_args(args: list) -> argparse.Namespace:
    """
    Get arguments from command line.

    Parameters
    ----------
    args: list
        Arguments passed to the program from the commandline.

    """
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", type=float, help="Adds a new coin to the list of"
                    " coins to be dispensed.  It must be an int.")
    ap.add_argument("--addlist", help="Adds a list of new coins to "
                    "the default list of coins to be dispensed. Format must be"
                    " a valid python datatype. e.g. using [x, y]")
    args = ap.parse_args(args)

    return args


def extend_coins(coins, args):
    """
    Extend the default coins with new coins to dispense.

    Parameters
    ----------
    coins: list
        The list of default coins.  [.25, .10, .05, .01]
    args: argparse.Namespace
        The arguments from argparse after the commandline arguments have been
        passed.

    Returns
    -------
    list:
        The list of coins that may have had optional arguments passed to them
        and added to the list of coins.
    """

    if args.add:
        coins.append(args.add)

    if args.addlist:
        try:
            # ast.literal_eval will evaluate the string datatype to literal
            # python datatype.  Then coins will add each item to itself.
            coins.extend(ast.literal_eval(args.addlist))

            # filter out strings that do not evalute to ints or floats
            coins = list(filter(lambda x: type(x) != str, coins))
        except SyntaxError:
            print("\nInvalid Argument: {} is not a valid datatype.  Try "
                  "something similar to [.4,.3] next time, ignoring argument "
                  "for now.\n".format(args.addlist))

    # sorted uses a timsort so it will be faster than what I come up with.
    coins = sorted(coins, reverse=True)

    return coins


def main():
    """Script entry point."""
    args = get_args(sys.argv[1:])

    coins = [.25, .10, .05, .01]

    coins = extend_coins(coins, args)
    money_input = get_input()
    totals_dict = dispense_coins(money_input, coins)

    print("\n{:-^25}\n".format("OUTPUT"))
    for coin in coins:
        print("{:{width}}: {} coins".format(str(coin), str(totals_dict[coin]),
              width=5))


if __name__ == "__main__":
    main()
