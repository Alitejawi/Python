#!/usr/bin/env python3

__author__ = "Ali Al-Itejawi"
__version__ = "1.1"
__email__ = "ali@al-itejawi.com"

__description__ = "Finds if an integer is even or odd in a range"

def is_odd(n):
    return n % 2

# Checking the first 20 numbers
for x in range(20):
    print(x, "is",
    "odd" if is_odd(x)
    else "even")