import argparse
from pprint import pprint

from file import FileUtil
from stats import StatsUtil


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
        cards = FileUtil.loadFromFiles(only=name)
        cardsStats = StatsUtil.getCardsStats(cards, exclPrice=exclPrice)
        setStats = StatsUtil.getSetStats(name, cardsStats, exclPrice=exclPrice)

        print(name)
        print('-' * len(name))
        StatsUtil.printSetStats(setStats)
        return

    setNameToSetCards = FileUtil.loadFromFiles()

    setNameToBoxEVs = {}

    setNamesSorted = sorted(list(setNameToSetCards.keys()))

    for setName in setNamesSorted:
        cards = setNameToSetCards[setName]
        cardsStats = StatsUtil.getCardsStats(cards, exclPrice=exclPrice)
        setStats = StatsUtil.getSetStats(setName, cardsStats, exclPrice=exclPrice)
        setNameToBoxEVs[setName] = setStats

    # pprint(setNameToBoxEVs)
    for setName in setNamesSorted:
        evs = setNameToBoxEVs[setName]

        print(setName)
        print('-' * len(setName))
        StatsUtil.printSetStats(evs)


def reportSet(args):
    setName = args.name

    cards = FileUtil.loadFromFiles(only=setName)
    stats = StatsUtil.getCardsStats(cards)

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
    for name in FileUtil.sets:
        s = FileUtil.sets[name]
        code = s['code']

        cards = FileUtil.getCardsForSet(code)
        with open(name, 'w') as f:
            f.write(json.dumps(cards))


main()

