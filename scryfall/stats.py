import statistics
from scipy.stats import kurtosis
from scipy.stats import skew

from file import FileUtil

class StatsUtil(object):
    """
    Houses useful methods for files.
    """

    @staticmethod
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

                    p = {
                        'mythic':   1.0 / 8.0,
                        'rare':     7.0 / 8.0,
                        'uncommon': 3.0,
                        'common':   10.0,
                    }[rarity]

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

    @staticmethod
    def getSetStats(setName, cardsStats, exclPrice=0):
        ret = {}

        nPacks = FileUtil.sets[setName]['nPacks']

        #
        # Calculate overall expected values
        #
        if (exclPrice > 0):
            # Average of cards that meet minimum price
            totalVA = 0.0
            for rarity in cardsStats:
                bucket = cardsStats[rarity]
                totalVA += bucket['exclusive']['avgValAdd']

            ret['exAvg'] = totalVA * nPacks
            # print('Exclusive EV by avg: %s' % totalVA)
            # print('\t(%s per box)\n' % (totalVA * nPacks))
        else:
            ret['exAvg'] = None

        # Average of all cards
        totalVA = 0.0
        for rarity in cardsStats:
            bucket = cardsStats[rarity]
            totalVA += bucket['all']['avgValAdd']

        ret['allAvg'] = totalVA * nPacks
        # print('All EV by avg: %s' % totalVA)
        # print('\t(%s per box)\n' % (totalVA * nPacks))

        # Median of all cards
        totalVA = 0.0
        for rarity in cardsStats:
            bucket = cardsStats[rarity]
            totalVA += bucket['all']['medValAdd']

        ret['allMed'] = totalVA * nPacks
        # print('All EV by med: %s' % totalVA)
        # print('\t(%s per box)\n' % (totalVA * nPacks))

        # from pprint import pprint
        # pprint(cardsStats)
        # exit()

        # Skewness
        mythicPriceValues = list(cardsStats['mythic']['all']['prices'].values())
        rarePriceValues   = list(cardsStats['rare']['all']['prices'].values())
        ret['m kurt'] = kurtosis(mythicPriceValues)
        ret['m skew'] = skew(mythicPriceValues)
        ret['r kurt'] = kurtosis(rarePriceValues)
        ret['r skew'] = skew(rarePriceValues)


        return ret

    @staticmethod
    def printSetStats(setStats):
        sortedEVs = sorted(list(setStats.keys()))
        for ev in sortedEVs:
            val = setStats[ev]
            ds = '$' if (ev not in ['m kurt', 'm skew', 'r kurt', 'r skew']) else ''

            if (ev == 'exAvg' and val == None):
                continue
            else:
                print('%s\t%s%.2f' % (ev, ds, val))

        print('\n')