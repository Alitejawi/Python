#!/usr/bin/env python3

__author__ = "Ali Al-Itejawi"
__version__ = "1.1"
__email__ = "ali@al-itejawi.com"

__description__ = "Concatenate a few strings from a list to a single string"

data = [
    "This", "is",
    "a", "sample", "message"
]

str = " ".join(data)
print(str)