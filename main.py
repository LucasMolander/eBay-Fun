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

def getMedian(card):
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



    #
    # TEMPORARY:
    #
    # Try just taking the median of the five most recently-finished auctions.
    #
    if (len(priceNumbers) > 5):
        priceNumbers = priceNumbers[0:5]


    if (len(priceNumbers) > 0):
        return statistics.median(priceNumbers)
    else:
        return 0

def reportExpansion(pathToFile):
    with open(pathToFile, 'r') as inFile:
        rawContents = inFile.read().split('\n')

    # This information is true regardless of the pack (Shards of Alara on).
    pMythic   = 1.0 / 8.0
    pRare     = 7.0 / 8.0
    pUncommon = 3.0
    pCommon   = 10.0

    # Let's just let the foil multiplier be 2 for now
    foilMultiplier = 2.0

    # Get some basic info from the top of the file
    setName = rawContents[0]
    packsPerBox = int(rawContents[1])
    pFoil = float(rawContents[2])

    print('\nCalculating the price of a ' + setName + ' booster box\n')

    nMythics = int(rawContents[3])
    nRares = int(rawContents[4])
    nUncommons = int(rawContents[5])
    nCommons = int(rawContents[6])
    nAll = nMythics + nRares + nUncommons + nCommons

    # Get indices for the cards
    mStart = 8
    mEnd = rawContents.index('RARES') - 1

    rStart = mEnd + 2
    rEnd = rawContents.index('UNCOMMONS') - 1

    uStart = rEnd + 2
    uEnd = rawContents.index('COMMONS') - 1

    cStart = uEnd + 2
    cEnd = len(rawContents) - 1

    # Assign the cards
    mythicNames = []
    rareNames = []
    uncommonNames = []
    commonNames = []

    for i in range(mStart, mEnd + 1):
        mythicNames.append(rawContents[i])

    for i in range(rStart, rEnd + 1):
        rareNames.append(rawContents[i])

    for i in range(uStart, uEnd + 1):
        uncommonNames.append(rawContents[i])

    for i in range(cStart, cEnd + 1):
        commonNames.append(rawContents[i])

    # # Print them out (for debugging purposes, for now)
    # print('MYTHICS:')
    # for n in mythicNames:
    #     print(n)
    # print('\n\nRARES:')
    # for n in rareNames:
    #     print(n)
    # print('\n\nUNCOMMONS:')
    # for n in uncommonNames:
    #     print(n)
    # print('\n\nCOMMONS:')
    # for n in commonNames:
    #     print(n)

    # Figure out the prices!
    mythicPrices = []
    rarePrices = []
    uncommonPrices = []
    commonPrices = []

    print('Mythic prices:')
    for name in mythicNames:
        med = getMedian(name + ' ' + setName)
        mythicPrices.append(med)

        # Debugging!
        print(str(round(med, 2)) + '\t' + name)
        sys.stdout.flush()

    print('\n\nRare prices:')
    for name in rareNames:
        med = getMedian(name + ' ' + setName)
        rarePrices.append(med)

        # Debugging!
        print(str(round(med, 2)) + '\t' + name)
        sys.stdout.flush()

    print('\n\nUncommon prices:')
    for name in uncommonNames:
        med = getMedian(name + ' ' + setName)
        uncommonPrices.append(med)

        # Debugging!
        print(str(round(med, 2)) + '\t' + name)
        sys.stdout.flush()

    print('\n\nCommon prices:')
    for name in commonNames:
        med = getMedian(name + ' ' + setName)
        commonPrices.append(med)

        # Debugging!
        print(str(round(med, 2)) + '\t' + name)
        sys.stdout.flush()

    # Averages
    mythicTotal = sum(mythicPrices)
    rareTotal = sum(rarePrices)
    commonTotal = sum(uncommonPrices)
    uncommonTotal = sum(commonPrices)
    allTotal = mythicTotal + rareTotal + commonTotal + uncommonTotal

    evMythic   = mythicTotal   / float(nMythics)
    evRare     = rareTotal     / float(nRares)
    evUncommon = commonTotal   / float(nUncommons)
    evCommon   = uncommonTotal / float(nCommons)

    print('\n\n')
    print('Expected Mythic price:   ' + str(round(evMythic, 2)))
    print('Expected Rare price:     ' + str(round(evRare, 2)))
    print('Expected Uncommon price: ' + str(round(evUncommon, 2)))
    print('Expected common price:   ' + str(round(evCommon, 2)))

    evRandom = allTotal / float(nAll)
    evFoil = evRandom * foilMultiplier

    print('Expected foil price:     ' + str(round(evFoil, 2)))

    evPerPack = (evMythic   * pMythic   +
                 evRare     * pRare     +
                 evUncommon * pUncommon +
                 evCommon   * pCommon   +
                 evFoil     * pFoil)

    print('\n\nExpected value per pack: ' + str(round(evPerPack, 2)))

    evPerBox = evPerPack * packsPerBox
    print('\n\nExpected value per box:  ' + str(round(evPerBox, 2)))




import sys
import requests
import re
import statistics



# reportExpansion('Expansions/Modern Masters 2017.txt')
# reportExpansion('Expansions/Shadows Over Innistrad.txt')
# reportExpansion('Expansions/Iconic Masters.txt')
# reportExpansion('Expansions/Modern Masters 2015.txt')
reportExpansion('Expansions/Modern Masters 2013.txt')




# jaceMedian = getMedian('Jace, the Mind Sculptor Worldwake')
# print('\n\n\n\n\nJace median:')
# print(jaceMedian)





# with open('Modern Masters 2013 RARES.txt', 'r') as inFile:
#     cards = inFile.read().split('\n')

# setName = cards[0]
# del cards[0]

# print('\nCards of note in ' + setName + ':')
# for card in cards:
#     med = getMedian(card + ' ' + setName)
#     print(str(med) + '\t' + card)
#     sys.stdout.flush() # These might take a while






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


