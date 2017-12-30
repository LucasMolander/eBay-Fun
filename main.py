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
    # if (len(priceNumbers) > 5):
    #     priceNumbers = priceNumbers[0:5]


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
    allNames = []      # Work for multithreading

    for i in range(mStart, mEnd + 1):
        mythicNames.append(rawContents[i])
        allNames.append(rawContents[i])

    for i in range(rStart, rEnd + 1):
        rareNames.append(rawContents[i])
        allNames.append(rawContents[i])

    for i in range(uStart, uEnd + 1):
        uncommonNames.append(rawContents[i])
        allNames.append(rawContents[i])

    for i in range(cStart, cEnd + 1):
        commonNames.append(rawContents[i])
        allNames.append(rawContents[i])

    # Figure out the prices
    # In a multithreaded way, of course. See the README for details.
    pool = ThreadPool(8)
    allPrices = pool.map(getMedian, allNames)

    # Put the prices back into their categories.
    cur = 0
    nxt = len(mythicNames)
    mythicPrices = allPrices[cur:nxt]

    cur  = nxt
    nxt += len(rareNames)
    rarePrices = allPrices[cur:nxt]

    cur  = nxt
    nxt += len(uncommonNames)
    uncommonPrices = allPrices[cur:nxt]

    cur  = nxt
    nxt += len(commonNames)
    commonPrices = allPrices[cur:nxt]

    # Print them out
    print('Mythic prices:')
    for i in range(0, len(mythicNames)):
        print(str(round(mythicPrices[i], 2)) + '\t' + mythicNames[i])
        sys.stdout.flush()

    print('\n\nRare prices:')
    for i in range(0, len(rareNames)):
        print(str(round(rarePrices[i], 2)) + '\t' + rareNames[i])
        sys.stdout.flush()

    print('\n\nUncommon prices:')
    for i in range(0, len(uncommonNames)):
        print(str(round(uncommonPrices[i], 2)) + '\t' + uncommonNames[i])
        sys.stdout.flush()

    print('\n\nCommon prices:')
    for i in range(0, len(commonNames)):
        print(str(round(commonPrices[i], 2)) + '\t' + commonNames[i])
        sys.stdout.flush()

    # Averages
    mythicTotal   = sum(mythicPrices)
    rareTotal     = sum(rarePrices)
    commonTotal   = sum(uncommonPrices)
    uncommonTotal = sum(commonPrices)
    allTotal      = mythicTotal + rareTotal + commonTotal + uncommonTotal

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

    print('\nMythics add:   ' + str(round((evMythic   * pMythic),   2)))
    print(  'Rares add:     ' + str(round((evRare     * pRare),     2)))
    print(  'Uncommons add: ' + str(round((evUncommon * pUncommon), 2)))
    print(  'Commons add:   ' + str(round((evCommon   * pCommon),   2)))
    print(  'Foils add:     ' + str(round((evFoil     * pFoil),     2)))

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
from multiprocessing.dummy import Pool as ThreadPool

reportExpansion('Expansions/Eternal Masters.txt')
