#!/usr/bin/env python3

__author__ = "Ali Al-Itejawi"
__version__ = "1.1"
__email__ = "ali@al-itejawi.com"

__description__ = "Slicing parts of a variable"

txt = 'Hello, Great World'

my_slice = slice(3,10)
print(txt[my_slice])

txt = 'Another string to be sliced'
print(txt[my_slice])