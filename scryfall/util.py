import urllib
import requests
import json
import sys
import statistics
import copy
from pprint import pprint

#
# Call this one more often.
#
def reportExpectedValues(exclPrice=0):
    setNameToSetCards = _loadFromFiles()

    setNameToBoxEVs = {}

    setNamesSorted = sorted(list(setNameToSetCards.keys()))

    for setName in setNamesSorted:
        cards = setNameToSetCards[setName]
        setStats = getSetStats(setName, cards, exclPrice=exclPrice)
        setNameToBoxEVs[setName] = setStats

    print('\nBoxes and their expected values:')
    if (exclPrice > 0):
        print('(EXCLUSIVE PRICE $%s)' % exclPrice)
    print('')
    # pprint(setNameToBoxEVs)
    for setName in setNamesSorted:
        evs = setNameToBoxEVs[setName]

        print(setName)
        print('-' * len(setName))
        for ev in evs:
            print('%s\t%s' % (ev, evs[ev]))
        print('\n')


def _loadFromFiles():
    nameToCards = {}

    for name in nameToCode:
        with open(name, 'r') as f:
            cards = json.loads(f.read())

        nameToCards[name] = cards

    return nameToCards


#
# Call this only every once in a while.
#
def storeToFiles():
    for name in nameToCode:
        code = nameToCode[name]

        cards = _getCardsForSet(code)
        with open(name, 'w') as f:
            f.write(json.dumps(cards))


def _getCardsForSet(code):
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
    print('Getting %d cards for %s' % (nCards, code))
    sys.stdout.flush()

    # Might be pagified
    while (response['has_more'] == True):
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

    return ret


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
    'Ixalan':                 'xln'
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
    'Ixalan':                 36
}

rarityToProbability = {
    'mythic':   1.0 / 8.0,
    'rare':     7.0 / 8.0,
    'uncommon': 3.0,
    'common':   10.0,
}


#
# Call either:
# reportExpectedValues()
# or
# storeToFiles()
#
def main():
    reportExpectedValues(exclPrice=2)

    # setStats = getSetStats('Iconic Masters', exclPrice=2)
    # pprint(setStats)

    
main()

#
# Eternal Masters:
#   0:  248
#   5:  159
#   10: 142
#   15: 126
#   20: 107
#
