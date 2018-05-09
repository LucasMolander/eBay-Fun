import re
import requests
import statistics

from html_parsing import removeOffersTaken, \
                         removeContaining,  \
                         removeNotContaining

from util import pricesToNumbers, priceToStr

import sys
import threading

from file_parsing import parseExpansionFile
# from find_prices import getMedianPriceSold



"""
Gets the 'sold auctions' HTML for a given item (with search gurads)
"""
def getHTML(item, guards, tIndex, out):
    #
    # Perform a GET request for the web page.
    #
    searchURL  = 'https://www.ebay.com/sch/i.html' # Base 'search' URL
    searchURL += '?&LH_Complete=1&LH_Sold=1'       # Sold auctions only
    searchURL += '&_nkw='                          # Put search string here

    searchString  = item
    for g in guards:
        searchString += ' -' + g
    searchString = re.sub(r' ', '%20', searchString)
    searchString = re.sub(r"'", '%27', searchString)

    finalURL = searchURL + searchString

    r = requests.get(finalURL)

    out[tIndex] = r.text



"""
Given the HTML from getHTML,
gets the median price of the last few 'sold' items on ebay.

@param item the item to search for
"""
def getMedianPriceSold(HTML, removes, requires, tIndex, out):


    #
    # Clean the page up.
    #
    HTML = HTML.encode('ascii', 'ignore')
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

    # Extra, more specific strings to be careful of in the title.
    # For example, we want to avoid '2017' for Modern Masters 2013.
    removeContaining(titles, prices, removes)

    # Also, we sometimes need to ensure that certain strings are in the title.
    # For example, if we are searching for a foil card, we want 'foil'.
    removeNotContaining(titles, prices, requires)

    # Turn strings into actual numebers.
    priceNumbers = pricesToNumbers(prices)



    #
    # Try just taking the median of the most recently-finished auctions.
    #
    medianCutoff = 20
    if (len(priceNumbers) > medianCutoff):
        priceNumbers = priceNumbers[0:medianCutoff]

    if (len(priceNumbers) > 0):
        out[tIndex] = statistics.median(priceNumbers)
    else:
        out[tIndex] = 0.0



def reportMTGBox(folder, file):

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

    # Guards to subtract in the search string. Less stringent than removes,
    # because if the search is unsuccessful, it'll do a different search.
    guards = ['4x', 'x4', '3x', 'x3', '2x', 'x2', 'playset']

    # Set-specific 'removes' it to be extra careful of
    if setName == 'Modern Masters 2013':
        removes = ['2015', '2017', 'MM15', 'MM17']
    elif setName == 'Modern Masters 2015':
        removes = ['2013', '2017', 'MM13', 'MM17']
    elif setName == 'Modern Masters 2017':
        removes = ['2013', '2015', 'MM13', 'MM15']
    elif setName == 'Innistrad':
        removes = ['shadows', 'over']
    else:
        removes = []

    # The auction should have the set name in the title
    requires = [setName]



    #
    # First, get the HTML
    # (in a threaded way)
    #

    # Threads will put HTML here
    HTML     = ['' for i in range(0, len(allNames))]
    HTMLFoil = ['' for i in range(0, len(allNames))]

    nfThreads = [] # Non-foil threads
    fThreads  = [] # Foil threads

    i = -1
    for n in allNames:
        i += 1

        # Arguments: item, removes, tIndex, out
        nfItem = n + ' ' + setName + ' -foil'
        fItem  = n + ' ' + setName + ' foil'

        nfArgs = (nfItem, guards, i, HTML)
        fArgs  = (fItem,  guards, i, HTMLFoil)

        nfT = threading.Thread(target=getHTML, args=nfArgs)
        fT  = threading.Thread(target=getHTML, args=fArgs)

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
    # Then, use the HTML to calculate the prices
    # (in a threaded way)
    #

    # Threads will put data here
    allPrices     = [0.0 for i in range(0, len(allNames))]
    allPricesFoil = [0.0 for i in range(0, len(allNames))]

    nfThreads = [] # Non-foil threads
    fThreads  = [] # Foil threads

    i = -1
    for n in allNames:
        i += 1

        nfHTML = HTML[i]
        fHTML  = HTMLFoil[i]

        nfRemoves = removes + ['foil']
        fRemoves = removes

        nfRequires = requires
        fRequires = requires + ['foil']

        nfArgs = (nfHTML, nfRemoves, nfRequires, i, allPrices)
        fArgs  = (fHTML,  fRemoves,  fRequires,  i, allPricesFoil)

        nfT = threading.Thread(target=getMedianPriceSold, args=nfArgs)
        fT  = threading.Thread(target=getMedianPriceSold, args=fArgs)

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
    # Construct the report.
    #

    out = ''

    title = 'Calculating the price of a ' + setName + ' booster box'
    out += title + '\n'
    out += '-' * len(title) + '\n'

    out += '\nMYTHICS\n'
    if (len(mythicNames) == 0):
        out += '<none>\n'
    for i in range(0, len(mythicNames)):
        out += priceToStr(mythicPrices[i])     + '\t' + \
               priceToStr(mythicPricesFoil[i]) + '\t' + \
               mythicNames[i] + '\n'

    out += '\nRARES\n'
    if (len(rareNames) == 0):
        out += '<none>\n'
    for i in range(0, len(rareNames)):
        out += priceToStr(rarePrices[i])     + '\t' + \
               priceToStr(rarePricesFoil[i]) + '\t' + \
               rareNames[i] + '\n'

    out += '\nUNCOMMONS\n'
    if (len(uncommonNames) == 0):
        out += '<none>\n'
    for i in range(0, len(uncommonNames)):
        out += priceToStr(uncommonPrices[i])     + '\t' + \
               priceToStr(uncommonPricesFoil[i]) + '\t' + \
               uncommonNames[i] + '\n'

    out += '\nCOMMONS\n'
    if (len(commonNames) == 0):
        out += '<none>\n'
    for i in range(0, len(commonNames)):
        out += priceToStr(commonPrices[i])     + '\t' + \
               priceToStr(commonPricesFoil[i]) + '\t' + \
               commonNames[i] + '\n'

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

    out += '\n'
    out += 'Expected Mythic price:   ' + priceToStr(evMythic)   + '\n'
    out += 'Expected Rare price:     ' + priceToStr(evRare)     + '\n'
    out += 'Expected Uncommon price: ' + priceToStr(evUncommon) + '\n'
    out += 'Expected common price:   ' + priceToStr(evCommon)   + '\n'

    evRandom = allTotal / float(nAll)
    evFoil = evRandom * foilMultiplier

    out += '\nExpected foil price:     ' + priceToStr(evFoil) + '\n'
    out += '\t(Foil multiplier = '       + priceToStr(foilMultiplier) + ')\n'

    out += '\nMythics add:   ' + priceToStr(evMythic   * pMythic)   + '\n'
    out +=   'Rares add:     ' + priceToStr(evRare     * pRare)     + '\n'
    out +=   'Uncommons add: ' + priceToStr(evUncommon * pUncommon) + '\n'
    out +=   'Commons add:   ' + priceToStr(evCommon   * pCommon)   + '\n'
    out +=   'Foils add:     ' + priceToStr(evFoil     * pFoil)     + '\n'

    evPerPack = (evMythic   * pMythic   +
                 evRare     * pRare     +
                 evUncommon * pUncommon +
                 evCommon   * pCommon   +
                 evFoil     * pFoil)

    out += '\nExpected value per pack: ' + priceToStr(evPerPack)

    evPerBox = evPerPack * packsPerBox
    out += '\nExpected value per box:  ' + priceToStr(evPerBox)

    return evPerBox, out
