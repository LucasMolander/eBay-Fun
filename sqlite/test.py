from database import TableCRUD, InsertionWrapper, SelectWrapper, LoadMTGJSON

load = LoadMTGJSON()
load.loadIntoDB()

def testInsertionAndDeletion():
    tc = TableCRUD()
    iw = InsertionWrapper()
    sw = SelectWrapper()

    print(tc.dropTables()['message'])
    print(tc.createTables()['message'])

    mySets = [
        {
            'name':        'The Best Set Ever(TM)',
            'packsPerBox': 36,
            'pFoil':       1.0 / 6.0,
            'nMythics':    12,
            'nRares':      50,
            'nUncommons':  80,
            'nCommons':    120
        },
        {
            'name':        'A bad set :(',
            'packsPerBox': 24,
            'pFoil':       1.0,
            'nMythics':    14,
            'nRares':      69,
            'nUncommons':  690,
            'nCommons':    420
        }
    ]

    myCards = [
        {
            'cName': 'Bad Card',
            'sName': 'Set 1',
            'rarity': 'Mythic'
        },
        {
            'cName': 'Medium Card',
            'sName': 'Set 1',
            'rarity': 'Rare'
        },
        {
            'cName': 'Good Card',
            'sName': 'Set 2',
            'rarity': 'Rare'
        }
    ]

    for s in mySets:
        print(iw.insertSet(s)['message'])

    for c in myCards:
        print(iw.insertCard(c)['message'])

    r1 = sw.selectAllSets()
    if (r1['success']):
        print(r1['data'])
    else:
        print(r1['message'])

    r2 = sw.selectAllCards()
    if (r2['success']):
        print(r2['data'])
    else:
        print(r2['message'])

# testInsertionAndDeletion()
