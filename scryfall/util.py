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
def reportExpectedValues(minPrice=0):
    setNameToSetCards = _loadFromFiles()

    setNameToBoxEV = {}

    setNamesSorted = sorted(list(setNameToSetCards.keys()))

    for setName in setNamesSorted:
        cards = setNameToSetCards[setName]

        setReportTitle = '%s (%d cards total)' % (setName, len(cards))
        dashes = '-' * len(setReportTitle)
        print('\n%s\n%s' % (setReportTitle, dashes))

        evPerBox = getBoxEV(setName, cards, minPrice=minPrice)

        setNameToBoxEV[setName] = evPerBox

    print('\nBoxes and their expected values:')
    pprint(setNameToBoxEV)


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


def getCardsStats(cards, minPrice=0):
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

        if (price >= minPrice):
            bucket['exclusive']['n']           += 1
            bucket['exclusive']['prices'][name] = price

    for rarity in ret:
        bucket = ret[rarity]

        for subset in bucket:
            innerBucket = bucket[subset]

            priceValues = list(innerBucket['prices'].values())
            if (len(priceValues) > 0):
                innerBucket['priceSum'] = sum(priceValues)
                innerBucket['priceAvg'] = statistics.mean(priceValues)
                innerBucket['priceMed'] = statistics.median(priceValues)
            else:
                innerBucket['priceSum'] = 0.0
                innerBucket['priceAvg'] = 0.0
                innerBucket['priceMed'] = 0.0

    return ret

def getValueAdds(averages):
    ret = {}

    # This information is true regardless of the pack (Shards of Alara on).
    pMythic   = 1.0 / 8.0
    pRare     = 7.0 / 8.0
    pUncommon = 3.0
    pCommon   = 10.0

    ret['mythicsAdd']   = averages['avgMythicPrice']   * pMythic
    ret['raresAdd']     = averages['avgRarePrice']     * pRare
    ret['uncommonsAdd'] = averages['avgUncommonPrice'] * pUncommon
    ret['commonsAdd']   = averages['avgCommonPrice']   * pCommon

    return ret

def getBoxEV(setName, cards, minPrice=0):
    stats     = getCardsStats(cards, minPrice=minPrice)
    valueAdds = getValueAdds(stats)
    
    print('Averages:')
    pprint(averages)

    print('\nValue adds:')
    pprint(valueAdds)

    packsPerBox = nameToNPacks[setName]
    evPerPack = sum(list(valueAdds.values()))
    evPerBox = evPerPack * packsPerBox
    print('\nEV per pack: %.2f' % evPerPack)
    print('EV per box: %.2f\n\n' % evPerBox)

    return evPerBox

def reportSet(setName, minPrice=0):
    setNameToSetCards = _loadFromFiles()
    cards = setNameToSetCards['Eternal Masters']
    stats = getCardsStats(cards, minPrice=minPrice)

    title = setName + ((' (minPrice=%s)' % minPrice) if minPrice > 0 else '')
    print('\n%s\n%s' % (title, '-' * len(title)))

    for rarity in ['mythic', 'rare', 'uncommon', 'common']:
        print(rarity)
        bucket = stats[rarity]
        for innerBucket in bucket:

            if (minPrice == 0 and innerBucket == 'exclusive'):
                continue

            print('\t%s' % innerBucket)

            innerStats = copy.deepcopy(bucket[innerBucket])
            del innerStats['prices']

            for s in innerStats:
                print('\t\t%s: %s' % (s, innerStats[s]))
            
        print('')
            

    # pprint(stats)
    exit()

    print('Mythic total: %s (average = %s)' % (stats['mythicTotal'], averages['avgMythicPrice']))
    print('Rare total: %s (average = %s)' % (stats['mythicTotal'], averages['avgMythicPrice']))
    print('Mythic total: %s (average = %s)' % (stats['mythicTotal'], averages['avgMythicPrice']))
    print('Mythic total: %s (average = %s)' % (stats['mythicTotal'], averages['avgMythicPrice']))


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


#
# Call either:
# reportExpectedValues()
# or
# storeToFiles()
#
def main():
    # reportExpectedValues(minPrice=100)

    reportSet('Eternal Masters', minPrice=5)

    
main()

#
# Eternal Masters:
#   0:  248
#   5:  159
#   10: 142
#   15: 126
#   20: 107
#
