from database import TableCRUD, InsertionWrapper, SelectWrapper, LoadMTGJSON, InitialPopulator

from price import PriceScanner

# load = LoadMTGJSON()
# load.loadIntoDB()

def resetDB():
    tc = TableCRUD()

    print(tc.dropTables()['message'])
    print(tc.createTables()['message'])

def testBasicSchema():
    resetDB()

    myOldSets = [
        {
            'name':        'Old Set 1',
            'packsPerBox': 36,
            'nUncommons':  2,
            'nCommons':    6
        }
    ]

    myNewSets = [
        {
            'name':        'New Set 1',
            'packsPerBox': 36,
            'pFoil':       1.0 / 6.0,
            'nMythics':    12,
            'nRares':      50,
            'nUncommons':  80,
            'nCommons':    120
        },
        {
            'name':        'New Set 2',
            'packsPerBox': 24,
            'pFoil':       1.0,
            'nMythics':    14,
            'nRares':      69,
            'nUncommons':  690,
            'nCommons':    420
        }
    ]

    myOldCards = [
        {
            'cName': 'Medium Card',
            'sName': 'Old Set 1',
            'rarity': 'C11'
        },
        {
            'cName': 'Really Good Card',
            'sName': 'Old Set 1',
            'rarity': 'U2'
        },
        {
            'cName': 'Should not work',
            'sName': 'Old Set 1',
            'rarity': 'Mythic'
        }
    ]

    myNewCards = [
        {
            'cName': 'Bad Card',
            'sName': 'New Set 1',
            'rarity': 'Mythic'
        },
        {
            'cName': 'Okay Card',
            'sName': 'New Set 1',
            'rarity': 'Rare'
        },
        {
            'cName': 'Good Card',
            'sName': 'New Set 2',
            'rarity': 'Uncommon'
        },
        {
            'cName': 'Should not work',
            'sName': 'New Set 2',
            'rarity': 'U1'
        }
    ]

    for os in myOldSets:
        print(iw.insertOldSet(os)['message'])

    for ns in myNewSets:
        print(iw.insertNewSet(ns)['message'])

    for oc in myOldCards:
        print(iw.insertOldCard(oc)['message'])

    for nc in myNewCards:
        print(iw.insertNewCard(nc)['message'])

    r = sw.selectAllOldSets()
    if (r['success']):
        print(r['data'])
    else:
        print(r['message'])

    r = sw.selectAllNewSets()
    if (r['success']):
        print(r['data'])
    else:
        print(r['message'])

    r = sw.selectAllOldCards()
    if (r['success']):
        print(r['data'])
    else:
        print(r['message'])

    r = sw.selectAllNewCards()
    if (r['success']):
        print(r['data'])
    else:
        print(r['message'])

def testInsertingOldThings():
    resetDB()

    ip = InitialPopulator()
    sw = SelectWrapper()

    # Insert old sets
    ip.populateOldSets()

    r = sw.selectAllOldSets()
    if (r['success']):
        print(r['data'])
    else:
        print(r['message'])

    # Insert old cards
    ip.populateOldCards()

    r = sw.selectAllOldCards()
    if (r['success']):
        print('Length: {0}'.format(len(r['data'])))
    else:
        print(r['message'])


def testSelectingCardsForSets():
    sw = SelectWrapper()
    ret = sw.selectOldCardsForSet('Antiquities')
    print(ret['message'])
    data = ret['data']
    print(data)
    for d in data:
        print(d)

def testStoringPrices():
    ps = PriceScanner()
    # status = ps.storePricesForSet('Antiquities', True)
    status = ps.storePricesForSet('Arabian Nights', True)
    # print(status)

# testBasicSchema()
# testInsertingOldThings()

# testSelectingCardsForSets()



testStoringPrices()

