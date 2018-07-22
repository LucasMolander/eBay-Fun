from database import SelectWrapper
import threading
import re
import requests
import statistics
import sys
import copy
from html import HTMLParseUtil

class PriceScanner(object):

    def __init__(self):
        pass

    @staticmethod
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

        print(finalURL)

        print('Sending request...')
        sys.stdout.flush()
        r = requests.get(finalURL)
        print('GOT A RESPONSE!')
        sys.stdout.flush()

        out[tIndex] = r.text

    @staticmethod
    def parseHTML(HTML, removes, requires, tIndex, out):
        #
        # Clean the page up.
        #
        HTML = HTML.encode('ascii', 'ignore')
        HTML = HTML.replace('\t', '').replace('\r', '').replace('\n', '')

        # Remove some stuff that's been messing with the titles
        HTML = HTML.replace("<span class=\"LIGHT_HIGHLIGHT\">New Listing</span>", '')

        # print(HTML)




        #
        # TITLES:
        # Click this link to access This is the Title">This is the Title</a>
        #
        # DOLLARS:
        # class="bold bidsold"><span class="sboffer">$55.00</span></span></li>
        # class="bold bidsold">$50.00</span></li>
        #

        # OLD
        # titles = re.findall(r'(?<=Click this link to access )[^>]+(?=\">)', HTML)
        # prices = re.findall(r'(?<=bidsold\">)<?[^<]*(?=<)', HTML)
        titles = re.findall(r'(?<=<\/div>)[^<]*', HTML)
        prices = re.findall(r'(?<=POSITIVE">)[^<]*', HTML)

        



        # print('\n\nTITLES\n\n')

        # for t in titles:
        #     print(t)

        # print('\n\nPRICES\n\n')

        # for p in prices:
        #     print(p)

        if (len(titles) != len(prices)):
            print('THREAD INDEX {0}:\n{1} titles; {2} prices\n'.format(tIndex, len(titles), len(prices)))
            out[tIndex] = -1.0
            return

        # exit(1)



        # Don't want to consider offers that were taken. Need a definite price.
        HTMLParseUtil.removeOffersTaken(titles, prices)

        # Extra, more specific strings to be careful of in the title.
        # For example, we want to avoid '2017' for Modern Masters 2013.
        HTMLParseUtil.removeContaining(titles, prices, removes)

        # Also, we sometimes need to ensure that certain strings are in the title.
        # For example, if we are searching for a foil card, we want 'foil'.
        HTMLParseUtil.removeNotContaining(titles, prices, requires)

        # Turn strings into actual numebers.
        priceNumbers = [float(p[p.find('$')+1 : ]) for p in prices]

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

    @staticmethod
    def getGuards():
        return ['4x', 'x4', '3x', 'x3', '2x', 'x2', 'playset']

    @staticmethod
    def getRemoves(setName):
        if setName == 'Modern Masters':
            return ['2015', '2017', 'MM15', 'MM17', '15', '17']
        elif setName == 'Modern Masters 2015 Edition':
            return ['2013', '2017', 'MM13', 'MM17', '13', '17']
        elif setName == 'Modern Masters 2017 Edition':
            return ['2013', '2015', 'MM13', 'MM15', '13', '15']
        elif setName == 'Innistrad':
            return ['shadows', 'over']
        else:
            return []

    @staticmethod
    def getHTMLThreads(areFoil, setName, cards, guards, HTMLOut):
        threads = []

        for i in range(0, len(cards)):
            card = cards[i]

            # Arguments: item, guards, tIndex, out
            foilStr = 'foil' if areFoil else '-foil'
            item = card[0] + ' ' + setName + ' mtg ' + foilStr

            args = (item, guards, i, HTMLOut)

            print('{0}: {1}'.format(i, item))

            t = threading.Thread(target=PriceScanner.getHTML, args=args)
            threads.append(t)

        return threads

    @staticmethod
    def getParseThreads(areFoil, cards, removes, requires, HTMLs, pricesOut):
        threads = []

        for i in range(0, len(cards)):
            localRemoves  = copy.deepcopy(removes)
            localRequires = copy.deepcopy(requires)

            if (areFoil):
                localRequires.append('foil')
            else:
                localRemoves.append('foil')

            # Arguments: HTML, removes, requires, tIndex, out
            args = (HTMLs[i], localRemoves, localRequires, i, pricesOut)
            t = threading.Thread(target=PriceScanner.parseHTML, args=args)
            threads.append(t)

        return threads

    @staticmethod
    def runThreads(threads):
        for t in threads:
            t.start()

        for t in threads:
            t.join()
            del t

    def getPrices(self, setName, isOldSet, cards):
        # Guards to subtract in the search string. Less stringent than removes,
        # because if the search is unsuccessful, it'll do a different search.
        guards = PriceScanner.getGuards()

        # Helps remove noise for sets with similar names
        removes = PriceScanner.getRemoves(setName)

        # The auction should have the set name in the title
        requires = [setName]

        if (isOldSet):
            HTML = ['' for i in range(0, len(cards))]
            threads = PriceScanner.getHTMLThreads(False, setName, cards, guards, HTML)
            PriceScanner.runThreads(threads)

            prices = [0.0 for i in range(0, len(cards))]
            threads = PriceScanner.getParseThreads(False, cards, removes, requires, HTML, prices)
            PriceScanner.runThreads(threads)

            for i in range(0, len(cards)):
                cards[i].append(round(prices[i], 2))

            cards = sorted(cards, key=lambda card: card[3])

            for i in range(0, len(cards)):
                print(cards[i])

        else:
            print('\'Not old set\' path in getPrices() isn\'t implemented yet!')
            return []

    def storePricesForSet(self, setName, isOldSet):
        ret = {
            'success': True,
            'message': 'Successfully set the prices for ' + setName
        }

        # # TEST
        # cards = [['Urza\'s mine', 'Antiquities', 'C1']]
        # self.getPrices(setName, isOldSet, cards)
        # print(cards[0][3])

        # Actual shit
        sw = SelectWrapper()
        if (isOldSet):
            status = sw.selectOldCardsForSet(setName)
            if (status['success'] == False):
                ret['success'] = False
                ret['message'] = 'Failed to set the prices for ' + setName + \
                    '. Reason: ' + status['message']

            cards = status['data']
            for c in cards:
                print(c)

            self.getPrices(setName, isOldSet, cards)

        else:
            ret['success'] = False
            ret['message'] = 'Not implemented yet!'
            return ret
