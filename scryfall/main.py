import urllib
import requests
import json
import sys
import statistics
import copy
import argparse
from pprint import pprint
from scipy.stats import kurtosis
from scipy.stats import skew

#
# Call this one more often.
#
def reportExpectedValues(args):
    exclPrice = args.exclPrice
    name = args.setName

    print('\nBoxes and their expected values:')
    if (exclPrice > 0):
        print('(EXCLUSIVE PRICE $%s)' % exclPrice)
    print('')

    if (name):
        cards = _loadFromFiles(only=name)
        setStats = getSetStats(name, cards, exclPrice=exclPrice)

        print(name)
        print('-' * len(name))
        _print_set_stats(setStats)
        return

    setNameToSetCards = _loadFromFiles()

    setNameToBoxEVs = {}

    setNamesSorted = sorted(list(setNameToSetCards.keys()))

    for setName in setNamesSorted:
        cards = setNameToSetCards[setName]
        setStats = getSetStats(setName, cards, exclPrice=exclPrice)
        setNameToBoxEVs[setName] = setStats

    # pprint(setNameToBoxEVs)
    for setName in setNamesSorted:
        evs = setNameToBoxEVs[setName]

        print(setName)
        print('-' * len(setName))
        _print_set_stats(evs)
        

def _loadFromFiles(only=None):
    if (only):
        with open(only, 'r') as f:
            return json.loads(f.read())

    nameToCards = {}

    for name in nameToCode:
        with open(name, 'r') as f:
            cards = json.loads(f.read())

        nameToCards[name] = cards

    return nameToCards


#
# Call this only every once in a while.
#
def storeToFiles(args):
    for name in nameToCode:
        code = nameToCode[name]

        cards = _getCardsForSet(code)
        with open(name, 'w') as f:
            f.write(json.dumps(cards))


def _getCardsForSet(code):
    print('Getting cards for %s' % code)
    sys.stdout.flush()

    cards = []

    baseURL = 'https://api.scryfall.com/cards/search?q='
    query = urllib.quote_plus('set=%s' % code)

    finalURL = baseURL + query

    r = requests.get(finalURL)

    if (r.status_code != 200):
        print('Bad return status (' + r.status_code + ' != 200)! Returning none.')
        return None

    
    response = json.loads(r.text)
    cards.extend(response['data'])

    nCards = response['total_cards']

    # Might be pagified
    while (response['has_more'] == True):
        print('\tGetting more cards for %s...' % code)
        sys.stdout.flush()

        url = response['next_page']
        r = requests.get(url)

        if (r.status_code != 200):
            print('Bad return status (' + r.status_code + ' != 200)! Returning none.')
            return None

        response = json.loads(r.text)
        cards.extend(response['data'])

    return cards


def getCardsStats(cards, exclPrice=0):
    ret = {
        'mythic': {
            'all': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            },
            'exclusive': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            }
        },
        'rare': {
            'all': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            },
            'exclusive': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            }
        },
        'uncommon': {
            'all': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            },
            'exclusive': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            }
        },
        'common': {
            'all': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            },
            'exclusive': {
                'n': 0,
                'prices': {},
                'priceSum': 0.0,
                'priceAvg': 0.0,
                'priceMed': 0.0
            }
        }
    }

    for c in cards:
        name = c['name']
        price = float(c['usd']) if 'usd' in c else 0.0

        bucket = ret[c['rarity']]

        bucket['all']['n']           += 1
        bucket['all']['prices'][name] = price

        if (price >= exclPrice):
            bucket['exclusive']['n'] += 1 
            bucket['exclusive']['prices'][name] = price
        else:
            bucket['exclusive']['prices'][name] = 0

    for rarity in ret:
        bucket = ret[rarity]

        for subset in bucket:
            innerBucket = bucket[subset]

            priceValues = list(innerBucket['prices'].values())
            if (len(priceValues) > 0):

                p = rarityToProbability[rarity]

                innerBucket['sum']       = sum(priceValues)
                innerBucket['avg']       = statistics.mean(priceValues)
                innerBucket['med']       = statistics.median(priceValues)
                innerBucket['avgValAdd'] = innerBucket['avg'] * p
                innerBucket['medValAdd'] = innerBucket['med'] * p
            else:
                innerBucket['sum']       = 0.0
                innerBucket['avg']       = 0.0
                innerBucket['med']       = 0.0
                innerBucket['avgValAdd'] = 0.0
                innerBucket['medValAdd'] = 0.0

    return ret


def getSetStats(setName, cards, exclPrice=0):
    ret = {}

    stats = getCardsStats(cards, exclPrice=exclPrice)

    # title = setName + ((' (exclPrice=%s)' % exclPrice) if exclPrice > 0 else '')
    # print('\n%s\n%s' % (title, '-' * len(title)))

    # for rarity in stats:
    #     print(rarity)
    #     bucket = stats[rarity]
    #     for innerBucket in bucket:

    #         if (exclPrice == 0 and innerBucket == 'exclusive'):
    #             continue

    #         print('\t%s' % innerBucket)

    #         innerStats = copy.deepcopy(bucket[innerBucket])
    #         del innerStats['prices']

    #         for s in innerStats:
    #             print('\t\t%s: %s' % (s, innerStats[s]))
            
    #     print('')

    nPacks = nameToNPacks[setName]

    #
    # Calculate overall expected values
    #
    if (exclPrice > 0):
        # Average of cards that meet minimum price
        totalVA = 0.0
        for rarity in stats:
            bucket = stats[rarity]
            totalVA += bucket['exclusive']['avgValAdd']

        ret['exAvg'] = totalVA * nPacks
        # print('Exclusive EV by avg: %s' % totalVA)
        # print('\t(%s per box)\n' % (totalVA * nPacks))
    else:
        ret['exAvg'] = None

    # Average of all cards
    totalVA = 0.0
    for rarity in stats:
        bucket = stats[rarity]
        totalVA += bucket['all']['avgValAdd']

    ret['allAvg'] = totalVA * nPacks
    # print('All EV by avg: %s' % totalVA)
    # print('\t(%s per box)\n' % (totalVA * nPacks))

    # Median of all cards
    totalVA = 0.0
    for rarity in stats:
        bucket = stats[rarity]
        totalVA += bucket['all']['medValAdd']

    ret['allMed'] = totalVA * nPacks
    # print('All EV by med: %s' % totalVA)
    # print('\t(%s per box)\n' % (totalVA * nPacks))

    # Skewness
    for rarity in stats:
        allPriceValues = list(bucket['all']['prices'].values())
        ret['kurt'] = kurtosis(allPriceValues)
        ret['skew'] = skew(allPriceValues)

    return ret

def _print_set_stats(setStats):
    sortedEVs = sorted(list(setStats.keys()))
    for ev in sortedEVs:
        val = setStats[ev]
        ds = '$' if (ev not in ['kurt', 'skew']) else ''

        if (ev == 'exAvg' and val == None):
            continue
        else:
            print('%s\t%s%.2f' % (ev, ds, val))

    print('\n')

def reportSet(args):
    setName = args.name

    cards = _loadFromFiles(only=setName)

    stats = getCardsStats(cards)

    for rarity in ['mythic', 'rare', 'uncommon', 'common']:
        bucket = stats[rarity]
        descStats = bucket['all']
        cardToPrice = descStats['prices']

        print('\n%s\n%s' % (rarity, ('-' * len(rarity))))
        print('(avg=%.2f, med=%.2f)' % (descStats['avg'], descStats['med']))

        # Sort by price descending
        for key, value in sorted(cardToPrice.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
            print "%s: %s" % (key, value)

    print('')


nameToCode = {
    'Eternal Masters':        'ema',
    'Modern Masters':         'mma',
    'Modern Masters 2015':    'mm2',
    'Modern Masters 2017':    'mm3',
    'Iconic Masters':         'ima',
    'Masters 25':             'a25',
    'Worldwake':              'wwk',
    'Kaladesh':               'kld',
    'Scars of Mirrodin':      'som',
    'New Phyrexia':           'nph',
    'Coldsnap':               'csp',
    'Khans of Tarkir':        'ktk',
    'Zendikar':               'zen',
    'Innistrad':              'isd',
    'Dark Ascension':         'dka',
    'Avacyn Restored':        'avr',
    'Return to Ravnica':      'rtr',
    'Gatecrash':              'gtc',
    'Battle for Zendikar':    'bfz',
    'Aether Revolt':          'aer',
    'Shadows over Innistrad': 'soi',
    'Hour of Devastation':    'hou',
    'Amonkhet':               'akh',
    'Ixalan':                 'xln',
    'Magic Origins':          'ori'
}

nameToNPacks = {
    'Eternal Masters':        24,
    'Modern Masters':         24,
    'Modern Masters 2015':    24,
    'Modern Masters 2017':    24,
    'Iconic Masters':         24,
    'Masters 25':             24,
    'Worldwake':              36,
    'Kaladesh':               36,
    'Scars of Mirrodin':      36,
    'New Phyrexia':           36,
    'Coldsnap':               36,
    'Khans of Tarkir':        36,
    'Zendikar':               36,
    'Innistrad':              36,
    'Dark Ascension':         36,
    'Avacyn Restored':        36,
    'Return to Ravnica':      36,
    'Gatecrash':              36,
    'Battle for Zendikar':    36,
    'Aether Revolt':          36,
    'Shadows over Innistrad': 36,
    'Hour of Devastation':    36,
    'Amonkhet':               36,
    'Ixalan':                 36,
    'Magic Origins':          36
}

rarityToProbability = {
    'mythic':   1.0 / 8.0,
    'rare':     7.0 / 8.0,
    'uncommon': 3.0,
    'common':   10.0,
}


class Ev(object):
    pass


#
# Call either:
# reportExpectedValues()
# or
# reportSet('Set name')
# or
# storeToFiles()
#
def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_evs = subparsers.add_parser('evs')
    parser_evs.add_argument('--exclPrice', type=float, default=0.0)
    parser_evs.add_argument('--setName', type=str, default=None)
    parser_evs.set_defaults(func=reportExpectedValues)

    parser_evs = subparsers.add_parser('set')
    parser_evs.add_argument('--name', type=str, required=True)
    parser_evs.set_defaults(func=reportSet)

    parser_evs = subparsers.add_parser('store')
    parser_evs.set_defaults(func=storeToFiles)

    args = parser.parse_args()
    args.func(args)

    # storeToFiles()

    # reportExpectedValues(exclPrice=2)

    # setStats = getSetStats('Iconic Masters', exclPrice=2)
    # pprint(setStats)

    # reportSet('Masters 25')

main()

#
# Eternal Masters:
#   0:  248
#   5:  159
#   10: 142
#   15: 126
#   20: 107
#
