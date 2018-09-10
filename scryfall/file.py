import sys
import urllib
import requests
import json

class FileUtil(object):
    """
    Houses useful methods for files.
    """

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
        },
        'Dominaria': {
            'code':   'dom',
            'nPacks': 36,
            'old':    False
        }
    }

    @staticmethod
    def loadFromFiles(only=None):
        if (only):
            with open(only, 'r') as f:
                return json.loads(f.read())

        nameToCards = {}

        for name in FileUtil.sets:
            with open(name, 'r') as f:
                cards = json.loads(f.read())

            nameToCards[name] = cards

        return nameToCards

    @staticmethod
    def getCardsForSet(code):
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

