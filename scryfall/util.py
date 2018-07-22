import urllib
import requests
import json
import sys
from pprint import pprint

#
# Call this one more often.
#
def reportExpectedValues():
    setNameToSetCards = _loadFromFiles()

    setNameToBoxEV = {}

    for setName in setNameToSetCards:
        cards = setNameToSetCards[setName]

        setReportTitle = '%s (%d cards total)' % (setName, len(cards))
        dashes = '-' * len(setReportTitle)
        print('\n%s\n%s' % (setReportTitle, dashes))

        evPerBox = getBoxEV(setName, cards)

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


def getCardsStats(cards):

    ret = {
        'nMythics':       0,
        'nRares':         0,
        'nUncommons':     0,
        'nCommons':       0,
        'mythicTotal':    0.0,
        'rareTotal':      0.0,
        'uncommonTotal':  0.0,
        'commonTotal':    0.0,
        'mythicPrices':   {},   # Individual card prices
        'rarePrices':     {},   # Individual card prices
        'uncommonPrices': {},   # Individual card prices
        'commonPrices':   {}    # Individual card prices
    }

    for c in cards:
        name = c['name']
        price = float(c['usd']) if 'usd' in c else 0.0
        rarity = c['rarity']
        if (rarity == 'mythic'):
            ret['nMythics']          += 1
            ret['mythicTotal']       += price
            ret['mythicPrices'][name] = price
        elif (rarity == 'rare'):
            ret['nRares']          += 1
            ret['rareTotal']       += price
            ret['rarePrices'][name] = price
        elif (rarity == 'uncommon'):
            ret['nUncommons']          += 1
            ret['uncommonTotal']       += price
            ret['uncommonPrices'][name] = price
        elif (rarity == 'common'):
            ret['nCommons']          += 1
            ret['commonTotal']       += price
            ret['commonPrices'][name] = price

    return ret

def getAverages(cardStats):
    ret = {}

    ret['avgMythicPrice']   = cardStats['mythicTotal'] / cardStats['nMythics'] if (cardStats['nMythics'] != 0) else 0
    ret['avgRarePrice']     = cardStats['rareTotal'] / cardStats['nRares'] if (cardStats['nRares'] != 0) else 0
    ret['avgUncommonPrice'] = cardStats['uncommonTotal'] / cardStats['nUncommons'] if (cardStats['nUncommons'] != 0) else 0
    ret['avgCommonPrice']   = cardStats['commonTotal'] / cardStats['nCommons'] if (cardStats['nCommons'] != 0) else 0

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

def getBoxEV(setName, cards):
    stats     = getCardsStats(cards)
    averages  = getAverages(stats)
    valueAdds = getValueAdds(averages)
    
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
    reportExpectedValues()

    
    
main()
