"""
This file is for proofs of concept for different parts of the overall program.
    - Getting web requests to work
    - Calculating minimums/maximums of functions
    - Etc.
"""

"""
General notes:
    - How to identify a card in Yugioh:
        * ID

    - How to identify a card in MTG:
        * Name and Set

    - Determinants of price (for classiciation):
        * Grade
        * Condition (might only be in item description)
        * Multiplicity
        * Common alterations (e.g. "Altered art")
"""

def removeNonASCII(str):
    out = []

    for c in str:
        out.append(c if ord(c) <128 else '')

    return ''.join(out)

import requests
import re

searchURL = 'https://www.ebay.com/sch/i.html' # Base 'search' URL
searchURL += '?&LH_Complete=1&LH_Sold=1'      # Sold auctions only
searchURL += '&_nkw='                         # Put search string here

cardName = 'Jace, the Mind Sculptor'
cardName = re.sub(r' ', '%20', cardName)

# print("Search string:")
# print(searchString)
# exit()

finalURL = searchURL + cardName

# print("Final URL:")
# print(finalURL)

r = requests.get(finalURL)
HTML = removeNonASCII(r.text)

HTML = re.sub(r' ', '', HTML)
HTML = re.sub(r'\t', '', HTML)
HTML = re.sub(r'\n', '', HTML)

# print(HTML)

# Find things that look like: <span class="bold bidsold">$50.00</span>
matches = re.findall(r"bidsold\">\$\d*\.\d*</span>", HTML)
print(matches)
