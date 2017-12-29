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
        * Foil
        * Grade
        * Condition (might only be in item description)
        * Multiplicity
        * Common alterations (e.g. "Altered art")
"""

"""
Removes all non-ascii (less than 128) characters from a string.
"""
def removeNonASCII(str):
    out = []

    for c in str:
        out.append(c if ord(c) < 128 else '')

    return ''.join(out)

"""

"""
def printListNice(list):
    for elem in list:
        print(elem)


import requests
import re

#
# Perform a GET request for the web page.
#
searchURL = 'https://www.ebay.com/sch/i.html' # Base 'search' URL
searchURL += '?&LH_Complete=1&LH_Sold=1'      # Sold auctions only
searchURL += '&_nkw='                         # Put search string here

cardName = 'Jace, the Mind Sculptor Worldwake'
cardName = re.sub(r' ', '%20', cardName)

finalURL = searchURL + cardName

r = requests.get(finalURL)

#
# Clean the page up.
#
HTML = removeNonASCII(r.text)
HTML = HTML.replace('\t', '').replace('\r', '').replace('\n', '')

#
# TITLES:
# Click this link to access This is the Title">This is the Title</a>
#
# DOLLARS:
# class="bold bidsold"><span class="sboffer">$55.00</span></span></li>
# class="bold bidsold">$50.00</span></li>
#
titles = re.findall(r'(?<=Click this link to access )[^>]+(?=\">)', HTML)
prices = re.findall(r'(?<=bidsold\">)<?[^<]*(?=<)', HTML)

print(str(len(titles)) + " titles:")
printListNice(titles)

print(str(len(prices)) + " prices:")
printListNice(prices)