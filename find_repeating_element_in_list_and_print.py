#!/usr/bin/env python3

__author__ = "Ali Al-Itejawi"
__version__ = "1.1"
__email__ = "ali@al-itejawi.com"

__description__ = "Find the first repeating element in a list, print it and quit"

data = [3, 5, 7, 5, 9, 11]
# 5 is the answer here

seen = set()
for x in data:
    if x in seen:
        print(x)
        break
    seen.add(x)