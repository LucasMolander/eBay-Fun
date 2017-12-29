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

def removeOffersTaken(titles, prices):
    i = len(prices) - 1

    while i >= 0:
        if not (re.search(r'^\$\d+\.\d+$', prices[i])):
            del prices[i]
            del titles[i]
        i = i - 1


def pricesToNumbers(prices):
    out = []

    for price in prices:
        out.append(float(price[1:]))

    return out

def getMedianForSearchString(card):
    #
    # Perform a GET request for the web page.
    #
    searchURL = 'https://www.ebay.com/sch/i.html' # Base 'search' URL
    searchURL += '?&LH_Complete=1&LH_Sold=1'      # Sold auctions only
    searchURL += '&_nkw='                         # Put search string here

    searchString = card
    searchString += ' -foil -4x -x4 -3x -x3 -2x -x2' # Guards
    searchString = re.sub(r' ', '%20', searchString)

    finalURL = searchURL + searchString

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

    # Don't want to consider offers that were taken. Need a definite price.
    removeOffersTaken(titles, prices)

    # Turn them into actual numerics.
    priceNumbers = pricesToNumbers(prices)
    # for priceN in priceNumbers:
    #     print(priceN)

    # Just take the median for now
    return statistics.median(priceNumbers)

import sys
import requests
import re
import statistics

# jaceMedian = getMedianForSearchString('Jace, the Mind Sculptor Worldwake')
# print('\n\n\n\n\nJace median:')
# print(jaceMedian)

with open('Modern Masters 2013 RARES.txt', 'r') as inFile:
    cards = inFile.read().split('\n')

setName = cards[0]
del cards[0]

print('\nCards of note in ' + setName + ':')
for card in cards:
    med = getMedianForSearchString(card + ' ' + setName)
    print(str(med) + '\t' + card)
    sys.stdout.flush() # These might take a while


# #
# # Perform a GET request for the web page.
# #
# searchURL = 'https://www.ebay.com/sch/i.html' # Base 'search' URL
# searchURL += '?&LH_Complete=1&LH_Sold=1'      # Sold auctions only
# searchURL += '&_nkw='                         # Put search string here

# cardName = 'Jace, the Mind Sculptor Worldwake'
# cardName = re.sub(r' ', '%20', cardName)

# finalURL = searchURL + cardName

# r = requests.get(finalURL)

# #
# # Clean the page up.
# #
# HTML = removeNonASCII(r.text)
# HTML = HTML.replace('\t', '').replace('\r', '').replace('\n', '')

# #
# # TITLES:
# # Click this link to access This is the Title">This is the Title</a>
# #
# # DOLLARS:
# # class="bold bidsold"><span class="sboffer">$55.00</span></span></li>
# # class="bold bidsold">$50.00</span></li>
# #
# titles = re.findall(r'(?<=Click this link to access )[^>]+(?=\">)', HTML)
# prices = re.findall(r'(?<=bidsold\">)<?[^<]*(?=<)', HTML)

# # print(str(len(titles)) + " titles:")
# # for title in titles:
# #     print(title)

# # print("\n\n")

# # print(str(len(prices)) + " prices:")
# # for price in prices:
# #     print(price)



# #
# # Don't want to consider offers that were taken. Need a definite price.
# #
# removeOffersTaken(titles, prices)

# # print("\n\n\n\n\n")

# # print(str(len(titles)) + " titles:")
# # for title in titles:
# #     print(title)

# # print("\n\n")

# # print(str(len(prices)) + " prices:")
# # for price in prices:
# #     print(price)



# #
# # Turn them into actual numerics.
# #
# priceNumbers = pricesToNumbers(prices)
# for priceN in priceNumbers:
#     print(priceN)


