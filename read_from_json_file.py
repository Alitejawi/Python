#!/usr/bin/env python3

__author__ = "Ali Al-Itejawi"
__version__ = "1.1"
__email__ = "ali@al-itejawi.com"

__description__ = "This script will allow you to read data from a JSON file, naming your JSON file capitals.json."

import json

with open('capitals.json') as f:
    data = json.load(f)

    for x in data:
        print(
            x["country"], '-',
            x["capital"]
        )