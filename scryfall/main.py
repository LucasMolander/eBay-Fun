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



#
# TODO
#
# The map used to be called 'nameToCode'. Go through and update where that appeared!!!
#

# Name to set object, which has code, nPacks, and old
sets = {
    'Eternal Masters': {
        'code':   'ema',
        'nPacks': 24,
        'old':    False
    },
    'Modern Masters': {
        'code':   'mma',
        'nPacks': 24,
        'old':    False
    },
    'Modern Masters 2015': {
        'code':   'mm2',
        'nPacks': 24,
        'old':    False
    },
    'Modern Masters 2017': {
        'code':   'mm3',
        'nPacks': 24,
        'old':    False
    },
    'Iconic Masters': {
        'code':   'ima',
        'nPacks': 24,
        'old':    False
    },
    'Masters 25': {
        'code':   'a25',
        'nPacks': 24,
        'old':    False
    },
    'Worldwake': {
        'code':   'wwk',
        'nPacks': 36,
        'old':    False
    },
    'Kaladesh': {
        'code':   'kld',
        'nPacks': 36,
        'old':    False
    },
    'Scars of Mirrodin': {
        'code':   'som',
        'nPacks': 36,
        'old':    False
    },
    'New Phyrexia': {
        'code':   'nph',
        'nPacks': 36,
        'old':    False
    },
    'Coldsnap': {
        'code':   'csp',
        'nPacks': 36,
        'old':    False
    },
    'Khans of Tarkir': {
        'code':   'ktk',
        'nPacks': 36,
        'old':    False
    },
    'Zendikar': {
        'code':   'zen',
        'nPacks': 36,
        'old':    False
    },
    'Innistrad': {
        'code':   'isd',
        'nPacks': 36,
        'old':    False
    },
    'Dark Ascension': {
        'code':   'dka',
        'nPacks': 36,
        'old':    False
    },
    'Avacyn Restored': {
        'code':   'avr',
        'nPacks': 36,
        'old':    False
    },
    'Return to Ravnica': {
        'code':   'rtr',
        'nPacks': 36,
        'old':    False
    },
    'Gatecrash': {
        'code':   'gtc',
        'nPacks': 36,
        'old':    False
    },
    'Battle for Zendikar': {
        'code':   'bfz',
        'nPacks': 36,
        'old':    False
    },
    'Aether Revolt': {
        'code':   'aer',
        'nPacks': 36,
        'old':    False
    },
    'Shadows over Innistrad': {
        'code':   'soi',
        'nPacks': 36,
        'old':    False
    },
    'Hour of Devastation': {
        'code':   'hou',
        'nPacks': 36,
        'old':    False
    },
    'Amonkhet': {
        'code':   'akh',
        'nPacks': 36,
        'old':    False
    },
    'Ixalan': {
        'code':   'xln',
        'nPacks': 36,
        'old':    False
    },
    'Magic Origins': {
        'code':   'ori',
        'nPacks': 36,
        'old':    False
    },
    'Core Set 2019': {
        'code':   'm19',
        'nPacks': 36,
        'old':    False
    },
    'Magic 2011': {
        'code':   'm11',
        'nPacks': 36,
        'old':    False
    }
}

#
# TODO
# Care about this later
#
# nameToCodeOld = {
#     'Alpha':     'lea',
#     'Beta':      'leb',
#     'Unlimited': '2ed',
#     'Collector\'s Edition': 'ced',
#     'Arabian Nights': 'arn',
#     'Antiquities': 'atq',
#     'Revised': '3ed',
#     'Legends': 'leg',
#     'The Dark': 'drk',
#     'Fallen Empires': 'fem',
#     'Fourth Edition': '4ed',
#     'Ice Age': 'ice'
# }

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

def storeToFiles(args):
    for name in sets:
        s = sets[name]
        code = s['code']

        cards = _getCardsForSet(code)
        with open(name, 'w') as f:
            f.write(json.dumps(cards))


main()

