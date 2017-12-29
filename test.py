"""
This file contains short tests for sanity checks.
"""


import re

one = 'This\nHas\n\nA\n\n\nLot\nOf New Lines\n\n\n\n'

print(one)

one = re.sub(r'\n', '', one)
one = re.sub(r'e', '', one)

print(one)




one = 'This\nHas\n\nA\n\n\nLot\nOf New Lines\n\n\n\n'

print(one)

# one = re.sub(r'[\ne]', '', one)
one = one.replace('\n', '')
one = one.replace('e', '')

print(one)