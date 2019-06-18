# Worksmith Coding Task
[![Build Status](https://travis-ci.org/B2Gdevs/worksmith_coding_task.svg?branch=master)](https://travis-ci.org/B2Gdevs/worksmith_coding_task)

You’re tasked with creating a program for making change. Your program should take as
an input the amount of change to make (e.g. 4.50), and it should output the number of
each coin to dispense so that the fewest possible coins are dispensed. The available
coins for you to use are quarters (.25), dimes (.10), nickels (.05), and pennies (.01).

Optional:
Extend this program so that it will work for any coin denominations (e.g. 6 cent coins).

## Solution

This program uses python 3 and can have optional arguments.  The default coins that is always
used are .25, .10, .05, .01. To test and just use the default values run the script without arguments.

### Default usage
```
python dispense_change.py
```

### Adding 1 number
The ```--add``` argument will only add one numerical value.
```
python dispense_change.py --add .7
```

### Adding multiple numbers
The ```--addlist``` argument will take a composite datatype and similar to a list or tuple 
then it will extend the coin list.
```
python dispense_change.py --addlist [.7, .1, .3]
```

Both arguments can be used at the same time.
```
python dispense_change.py --addlist [.7, .1, .3] --add .15
```

### Information
The program will truncate long real numbers to the 2nd decimal place.  So the lowest number that can be added to the list
is already added by default since that is 0.01.  However, the inverse isn't constrained.  The positive value can continue to go up.
The reason being that I have been to japan where it was common to use a 500 yen coin which would be 5 dollars.
