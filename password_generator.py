#!/usr/bin/env python3

__author__ = "Ali Al-Itejawi"
__version__ = "1.0"
__email__ = "ali@al-itejawi.com"

__description__ = "Simple password generator using Python"

import random

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
symbols = "[]{}()*;/,_-"

all = lower+upper+numbers+symbols

length = 16
password = "".join(random.sample(all,length))
print(password)