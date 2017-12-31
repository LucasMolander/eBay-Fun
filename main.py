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

    - Determinants of price:
        * Foil
        * Grade
        * Condition (might only be in item description)
        * Multiplicity
        * Common alterations (e.g. "Altered art")
"""



"""
If it's not a foil, put ' -foil' in the card name.
If it IS a foil,     put  ' foil'  in the card name.
"""
def getMedian(card, setName, isFoil, removes, tIndex, out):

    #
    # Perform a GET request for the web page.
    #
    searchURL = 'https://www.ebay.com/sch/i.html' # Base 'search' URL
    searchURL += '?&LH_Complete=1&LH_Sold=1'      # Sold auctions only
    searchURL += '&_nkw='                         # Put search string here

    searchString  = card
    searchString += ' ' + setName
    searchString += (' foil' if isFoil else ' -foil')
    searchString += ' -4x -x4 -3x -x3 -2x -x2'    # Guards
    searchString = re.sub(r' ', '%20', searchString)
    searchString = re.sub(r"'", '%27', searchString)

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

    # If searching for a foil, remove cards that don't have 'foil' in the title.
    # If searching for a non-foil, remove titles that do have 'foil'.
    # removeOppositeFoility(titles, prices, isFoil)
    if isFoil:
        removeNotContaining(titles, prices, ['foil'])
    else:
        removeContaining(titles, prices, ['foil'])

    # Extra, more specific strings to be careful of in the title.
    # For example, we want to avoid '2017' for Modern Masters 2013.
    removeContaining(titles, prices, removes)

    # Turn them into actual numerics.
    priceNumbers = pricesToNumbers(prices)



    #
    # Try just taking the median of the five most recently-finished auctions.
    #
    medianCutoff = 10
    if (len(priceNumbers) > medianCutoff):
        priceNumbers = priceNumbers[0:medianCutoff]

    if (len(priceNumbers) > 0):
        # return statistics.median(priceNumbers)
        out[tIndex] = statistics.median(priceNumbers)
    else:
        out[tIndex] = 0.0

def reportExpansion(folder, file):

    #
    # Pre-processing. 
    #
    pathToFile = folder + '/' + file

    # Parse info about the set from the file.
    setInfo = parseExpansionFile(pathToFile)
    setName       = setInfo['setName']
    packsPerBox   = setInfo['packsPerBox']
    pFoil         = setInfo['pFoil']
    nMythics      = setInfo['nMythics']
    nRares        = setInfo['nRares']
    nUncommons    = setInfo['nUncommons']
    nCommons      = setInfo['nCommons']
    nAll          = setInfo['nAll']
    mythicNames   = setInfo['mythicNames']
    rareNames     = setInfo['rareNames']
    uncommonNames = setInfo['uncommonNames']
    commonNames   = setInfo['commonNames']
    allNames      = setInfo['allNames']

    # This information is true regardless of the pack (Shards of Alara on).
    pMythic   = 1.0 / 8.0
    pRare     = 7.0 / 8.0
    pUncommon = 3.0
    pCommon   = 10.0

    # Set-specific 'removes' it to be extra careful of
    removes = []

    if setName == 'Modern Masters 2013':
        removes.extend(['2015', '2017', 'MM15', 'MM17'])
    elif setName == 'Modern Masters 2015':
        removes.extend(['2013', '2017', 'MM13', 'MM17'])
    elif setName == 'Modern Masters 2017':
        removes.extend(['2013', '2015', 'MM13', 'MM15'])

    if setName == 'Innistrad':
        removes.extend(['shadows', 'over'])



    #
    # Threads.
    #

    # Threads will put info here
    allPrices = []
    allPricesFoil = []
    for i in range(0, len(allNames)):
        allPrices.append(0.0)
        allPricesFoil.append(0.0)

    nfThreads = [] # Non-foil threads
    fThreads = []  # Foil threads

    i = -1
    for n in allNames:
        i += 1

        # card, isFoil, removes, tIndex, out
        nfArgs = (n, setName, False, removes, i, allPrices)
        fArgs  = (n, setName, True,  removes, i, allPricesFoil)

        nfT = threading.Thread(target=getMedian, args=nfArgs)
        fT  = threading.Thread(target=getMedian, args=fArgs)

        nfThreads.append(nfT)
        fThreads.append(fT)

        nfT.start()
        fT.start()

    # Wait for all threads to be done.
    for t in nfThreads:
        t.join()
        del t
    for t in fThreads:
        t.join()
        del t



    #
    # Price and foil shenanigans.
    #

    if sum(allPrices) > 0.0:
        foilMultiplier = (sum(allPricesFoil) / sum(allPrices))
    else:
        foilMultiplier = 0.0

    # In case we couldn't find a foil card, just interpolate.
    # That is, if the foil price is 0, set it to:
    #     the median of the foil multipliers * its regular value
    foilMultipliers = []
    for i in range(0, len(allPricesFoil)):
        val = (allPricesFoil[i] / allPrices[i]) if allPrices[i] > 0.0 else 0.0
        foilMultipliers.append(val)

    medianFoilMultiplier = statistics.median(foilMultipliers)

    for i in range(0, len(allPricesFoil)):
        if allPricesFoil[i] == 0.0:
            allPricesFoil[i] = allPrices[i] * medianFoilMultiplier

    # Put the prices back into their categories.
    cur = 0
    nxt = len(mythicNames)
    mythicPrices = allPrices[cur:nxt]
    mythicPricesFoil = allPricesFoil[cur:nxt]

    cur  = nxt
    nxt += len(rareNames)
    rarePrices = allPrices[cur:nxt]
    rarePricesFoil = allPricesFoil[cur:nxt]

    cur  = nxt
    nxt += len(uncommonNames)
    uncommonPrices = allPrices[cur:nxt]
    uncommonPricesFoil = allPricesFoil[cur:nxt]

    cur  = nxt
    nxt += len(commonNames)
    commonPrices = allPrices[cur:nxt]
    commonPricesFoil = allPricesFoil[cur:nxt]



    #
    # Printing the report.
    #

    # Print them out
    print('Mythic prices:')
    for i in range(0, len(mythicNames)):
        print(str(round(mythicPrices[i], 2))     + '\t' + 
              str(round(mythicPricesFoil[i], 2)) + '\t' +
              mythicNames[i])

    print('\n\nRare prices:')
    for i in range(0, len(rareNames)):
        print(str(round(rarePrices[i], 2))     + '\t' + 
              str(round(rarePricesFoil[i], 2)) + '\t' +
              rareNames[i])

    print('\n\nUncommon prices:')
    for i in range(0, len(uncommonNames)):
        print(str(round(uncommonPrices[i], 2))     + '\t' + 
              str(round(uncommonPricesFoil[i], 2)) + '\t' +
              uncommonNames[i])

    print('\n\nCommon prices:')
    for i in range(0, len(commonNames)):
        print(str(round(commonPrices[i], 2))     + '\t' + 
              str(round(commonPricesFoil[i], 2)) + '\t' +
              commonNames[i])

    # Averages
    mythicTotal   = sum(mythicPrices)
    rareTotal     = sum(rarePrices)
    commonTotal   = sum(uncommonPrices)
    uncommonTotal = sum(commonPrices)
    allTotal      = mythicTotal + rareTotal + commonTotal + uncommonTotal

    evMythic   = (mythicTotal   / float(nMythics))   if nMythics   > 0 else 0.0
    evRare     = (rareTotal     / float(nRares))     if nRares     > 0 else 0.0
    evUncommon = (commonTotal   / float(nUncommons)) if nUncommons > 0 else 0.0
    evCommon   = (uncommonTotal / float(nCommons))   if nCommons   > 0 else 0.0

    print('\n\n')
    print('Expected Mythic price:   ' + str(round(evMythic, 2)))
    print('Expected Rare price:     ' + str(round(evRare, 2)))
    print('Expected Uncommon price: ' + str(round(evUncommon, 2)))
    print('Expected common price:   ' + str(round(evCommon, 2)))

    evRandom = allTotal / float(nAll)
    evFoil = evRandom * foilMultiplier

    print('Expected foil price:     ' + str(round(evFoil, 2)))
    print('\t(Foil multiplier = ' + str(round(foilMultiplier, 2)) + ')')

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

    return evPerBox




import sys
import requests
import re
import statistics
import threading

from file_parsing import parseExpansionFile

from html_parsing import removeNonASCII,    \
                         removeOffersTaken, \
                         removeContaining,  \
                         removeNotContaining

from util import pricesToNumbers

reportExpansion('Expansions', 'Rise of the Eldrazi.txt')



# #
# # Get a report for each of these expansions and write them to a file.
# #
# expansions = [
#     'Amonkhet',
#     'Eternal Masters',
#     'Hour of Devastation',
#     'Iconic Masters',
#     'Ixalan',
#     'Modern Masters 2013',
#     'Modern Masters 2015',
#     'Modern Masters 2017',
#     'Shadows Over Innistrad'
# ]

# expectedValues = []

# for e in expansions:
#     ev = reportExpansion('Expansions', e + '.txt')
#     expectedValues.append(ev)

# outFile = open('Expected Values/12.31.2017 3.txt', 'w')

# for i in range(0, len(expansions)):
#     outFile.write(expansions[i]+':\t'+str(round(expectedValues[i], 2))+'\n')

# outFile.close()

