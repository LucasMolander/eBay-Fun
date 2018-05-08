import sqlite3
import json

class DBUtil(object):

    @staticmethod
    def verifyArgs(args, reqiredArgs, ret):
        missing = []

        for ra in reqiredArgs:
            if (ra not in args):
                missing.append(ra)
        
        if (len(missing) > 0):
            ret['success'] = False
            ret['message'] = 'Missing required attributes in method argument. ' + \
                'Missing attribute(s): ' + ', '.join(missing)

        return (len(missing) == 0)

    @staticmethod
    def stripArgs(args, requiredArgs):
        stripped = []

        for i in range(0, len(requiredArgs)):
            stripped.append(args[requiredArgs[i]])

        return stripped

class SelectWrapper(object):

    #
    # SELECT statements.
    #
    selectAllOldSetsSQL  = "SELECT * FROM OldSets"
    selectAllNewSetsSQL  = "SELECT * FROM NewSets"
    selectAllOldCardsSQL = "SELECT * FROM OldCards"
    selectAllNewCardsSQL = "SELECT * FROM NewCards"

    def __init__(self):
        pass

    def selectAllOldSets(self):
        ret = {
            'success' : True,
            'message' : 'Successfully selected all old sets',
            'data' : None
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.selectAllOldSetsSQL)
            ret['data'] = c.fetchall()
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to select all old sets. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def selectAllNewSets(self):
        ret = {
            'success' : True,
            'message' : 'Successfully selected all new sets',
            'data' : None
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.selectAllNewSetsSQL)
            ret['data'] = c.fetchall()
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to select all new sets. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def selectAllOldCards(self):
        ret = {
            'success' : True,
            'message' : 'Successfully selected all old cards',
            'data' : None
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.selectAllOldCardsSQL)
            ret['data'] = c.fetchall()
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to select all old cards. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def selectAllNewCards(self):
        ret = {
            'success' : True,
            'message' : 'Successfully selected all new cards',
            'data' : None
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.selectAllNewCardsSQL)
            ret['data'] = c.fetchall()
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to select all new cards. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

class InsertionWrapper(object):

    #
    # INSERT INTO statements.
    #
    insertOldSetSQL = \
        "INSERT INTO OldSets "                               + \
        "(name, packsPerBox, nRares, nUncommons, nCommons) " + \
        "VALUES (?, ?, ?, ?, ?)"

    insertNewSetSQL = \
        "INSERT INTO NewSets "                                   + \
        "(name, pFoil, nMythics, nRares, nUncommons, nCommons) " + \
        "VALUES (?, ?, ?, ?, ?, ?)"

    insertOldCardSQL = \
        "INSERT INTO OldCards "   + \
        "(cName, sName, rarity) " + \
        "VALUES (?, ?, ?)"

    insertNewCardSQL = \
        "INSERT INTO NewCards "   + \
        "(cName, sName, rarity) " + \
        "VALUES (?, ?, ?)"

    def __init__(self):
        pass

    def insertOldSet(self, attributes):
        ret = {
            'success' : True,
            'message' : 'Successfully inserted old set'
        }

        # Verify that we have the correct arguments.
        requiredAttributes = ['name', 'packsPerBox', 'nRares', 'nUncommons', 'nCommons']
        
        if (not DBUtil.verifyArgs(attributes, requiredAttributes, ret)):
            return ret

        # And strip them down, and put them in order.
        strippedAttrs = DBUtil.stripArgs(attributes, requiredAttributes)

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.insertOldSetSQL, strippedAttrs)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to insert old set. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def insertNewSet(self, attributes):
        ret = {
            'success' : True,
            'message' : 'Successfully inserted new set'
        }

        # Verify that we have the correct arguments.
        requiredAttributes = ['name', 'pFoil', 'nMythics', 'nRares', 'nUncommons', 'nUncommons']
        
        if (not DBUtil.verifyArgs(attributes, requiredAttributes, ret)):
            return ret

        # And strip them down, and put them in order.
        strippedAttrs = DBUtil.stripArgs(attributes, requiredAttributes)

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.insertNewSetSQL, strippedAttrs)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to insert new set. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def insertOldCard(self, attributes):
        ret = {
            'success' : True,
            'message' : 'Successfully inserted old card'
        }

        # Verify that we have the correct arguments.
        requiredAttributes = ['cName', 'sName', 'rarity']

        if (not DBUtil.verifyArgs(attributes, requiredAttributes, ret)):
            return ret

        # And strip them down, and put them in order.
        strippedAttrs = DBUtil.stripArgs(attributes, requiredAttributes)

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.insertOldCardSQL, strippedAttrs)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to insert old card. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def insertNewCard(self, attributes):
        ret = {
            'success' : True,
            'message' : 'Successfully inserted new card'
        }

        # Verify that we have the correct arguments.
        requiredAttributes = ['cName', 'sName', 'rarity']

        if (not DBUtil.verifyArgs(attributes, requiredAttributes, ret)):
            return ret

        # And strip them down, and put them in order.
        strippedAttrs = DBUtil.stripArgs(attributes, requiredAttributes)

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.insertNewCardSQL, strippedAttrs)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to insert new card. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

class TableCRUD(object):

    #
    # CREATE TABLE statements.
    #
    createOldSetsTableSQL = \
        "CREATE TABLE OldSets ( "            + \
            "name        TEXT PRIMARY KEY, " + \
            "packsPerBox INTEGER, "          + \
            "nRares      INTEGER, "          + \
            "nUncommons  INTEGER, "          + \
            "nCommons    INTEGER "           + \
        ")"

    createNewSetsTableSQL = \
        "CREATE TABLE NewSets ( "            + \
            "name        TEXT PRIMARY KEY, " + \
            "packsPerBox INTEGER, "          + \
            "pFoil       REAL, "             + \
            "nMythics    INTEGER, "          + \
            "nRares      INTEGER, "          + \
            "nUncommons  INTEGER, "          + \
            "nCommons    INTEGER "           + \
        ")"

    createOldCardsTableSQL = \
        "CREATE TABLE OldCards ( "                           + \
            "cName  TEXT, "                                  + \
            "sName  TEXT, "                                  + \
            "rarity TEXT CHECK(rarity IN ( "                 + \
                "'U1', 'R1', 'U3', 'C1', 'U2', "             + \
                "'C2', 'C3', 'C4', 'C5', 'C11', 'U4' "       + \
            ")), "                                           + \
            "PRIMARY KEY (cName, sName), "                   + \
            "FOREIGN KEY (sName) REFERENCES OldSets (name) " + \
        ")"

    createNewCardsTableSQL = \
        "CREATE TABLE NewCards ( "                           + \
            "cName  TEXT, "                                  + \
            "sName  TEXT, "                                  + \
            "rarity TEXT CHECK(rarity IN "                   + \
                "('Mythic', 'Rare', 'Uncommon', 'Common') "  + \
            "), "                                            + \
            "PRIMARY KEY (cName, sName), "                   + \
            "FOREIGN KEY (sName) REFERENCES NewSets (name) " + \
        ")"

    #
    # DROP TABLE statements.
    #
    deleteOldSetsTableSQL  = "DROP TABLE OldSets"
    deleteNewSetsTableSQL  = "DROP TABLE NewSets"
    deleteOldCardsTableSQL = "DROP TABLE OldCards"
    deleteNewCardsTableSQL = "DROP TABLE NewCards"

    def __init__(self):
        pass

    def createTables(self):
        ret = {
            'success' : True,
            'message' : 'Successfully created tables'
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.createOldSetsTableSQL)
            c.execute(self.createNewSetsTableSQL)
            c.execute(self.createOldCardsTableSQL)
            c.execute(self.createNewCardsTableSQL)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to create tables. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def dropTables(self):
        ret = {
            'success' : True,
            'message' : 'Successfully dropped tables'
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.deleteOldCardsTableSQL)
            c.execute(self.deleteNewCardsTableSQL)
            c.execute(self.deleteOldSetsTableSQL)
            c.execute(self.deleteNewSetsTableSQL)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to drop tables. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

class LoadMTGJSON(object):

    filePath = 'AllSets.json'

    def __init__(self):
        pass

    def getJSONObject(self):
        try:
            with open(self.filePath, 'r') as f:
                contents = f.read()
                contents = contents.decode('utf-8')
                contents = contents.encode('ascii', 'ignore')
                data = json.loads(contents)
        except Exception as e:
            print(('Could not load file \'{0}\' due to error: \'{1}\'. ' + \
                'Exiting.').format(self.filePath, str(e)))
            exit(1)

        return data

    def trimSets(self, obj):
        keepTypes = ['core', 'masters', 'un', 'expansion', 'reprint', 'conspiracy']
        deleteReprints = ['Collector\'s Edition', 'International Collector\'s Edition']
        deleteTimeShift = ['Time Spiral', 'Time Spiral \"Timeshifted\"', 'Planar Chaos', 'Future Sight']

        deleteCodes = []

        for setCode in obj:
            setObj = obj[setCode]

            # Remove sets that aren't ones we want to keep
            if (setObj['type'] not in keepTypes):
                deleteCodes.append(setCode)
                continue

            # Further, only keep certain types of reprints (e.g. Modern Masters)
            if (setObj['type'] == 'reprint' and setObj['name'] in deleteReprints):
                deleteCodes.append(setCode)
                continue

            # Also, delete timeshifted wonkiness
            if (setObj['type'] == 'expansion' and setObj['name'] in deleteTimeShift):
                deleteCodes.append(setCode)
                continue

        for dc in deleteCodes:
            del obj[dc]

    #
    # Old packs are pretty screwey with how they handle rarity.
    # Make a <setName, <cardName, rarity>> map manually.
    #
    # SPECIAL - CHRONICLES
    # Chronicles:     Rare: U1.     Uncommon: U3, C1
    #
    # Arabian Nights: Rare: U2.     Uncommon: U3, U4
    # Fallen Empires: Rare: U1.     Uncommon: U2, U3
    # Antiquities:    Rare: U1.     Uncommon: U2, U3 (WEIRD)
    # Homelands:      Rare: U1.     Uncommon: U3, C1
    # The Dark:       Rare: U1, U2. Uncommon: <DNE>
    # Legends:        Rare: R1.     Uncommon: U1, U2
    #
    # Just say that The Dark is two rares, and they're U1, U2.
    # Make any 'uncommon' just be 'C1'
    #
    # ALSO, FINAL NOTE:
    # Watch some pack opening videos to make sure that this is consistent.
    #
    # Good website: https://magiccards.info/ch/en.html
    #
    def getSetAttribs(self, mtgSet):
        setName = mtgSet['name']

        theType = mtgSet['type']
        rares  = mtgSet['booster'][0]
        others = mtgSet['booster'][1:]

        nameCardsMap = {}
        cards = mtgSet['cards']        
        for c in cards:
            # Ignore basic lands
            if (c['rarity'] == 'Basic Land'):
                continue

            cardName = c['name']

            if (cardName not in nameCardsMap):
                nameCardsMap[cardName] = []

            nameCardsMap[cardName].append(c)

        for n in nameCardsMap:
            cards = nameCardsMap[n]
            if (len(cards) > 1):
                rarities = [c['rarity'] for c in cards]

                do = False
                for r in rarities:
                    if (r != rarities[0]):
                        do = True

                if (do):
                    print('{0} - {1}: {2}. {3}'.format(setName, n, len(cards), rarities))

    def loadIntoDB(self):
        self.buildRarityMap()
        exit()

        obj = self.getJSONObject()
        
        # types = {}

        # for setCode in obj:
        #     setObj = obj[setCode]

        #     setType = setObj['type']
        #     if (setType not in types):
        #         types[setType] = 0
        #     types[setType] += 1

        # for t in types:
        #     print('{0}: {1}'.format(t, types[t]))

        # print('\n----------\n')

        self.trimSets(obj)

        # types = {}

        # for setCode in obj:
        #     setObj = obj[setCode]

        #     setType = setObj['type']
        #     if (setType not in types):
        #         types[setType] = 0
        #     types[setType] += 1

        # for t in types:
        #     print('{0}: {1}'.format(t, types[t]))

        for setCode in obj:
            setObj = obj[setCode]

            attribs = self.getSetAttribs(setObj)
            # print(attribs)

class InitialPopulator(object):

    def __init__(self):
        pass

    def populateOldSets(self):
        sets = [
            {
                'name':        'Antiquities',
                'packsPerBox': 60,
                'nRares':      0,
                'nUncommons':  2,
                'nCommons':    6
            },
            {
                'name':        'Arabian Nights',
                'packsPerBox': 60,
                'nRares':      0,
                'nUncommons':  2,
                'nCommons':    6
            },
            {
                'name':        'Fallen Empires',
                'packsPerBox': 60,
                'nRares':      0,
                'nUncommons':  2,
                'nCommons':    6
            },
            {
                'name':        'Homelands',
                'packsPerBox': 60,
                'nRares':      0,
                'nUncommons':  2,
                'nCommons':    6
            },
            {
                'name':        'Legends',
                'packsPerBox': 36,
                'nRares':      1,
                'nUncommons':  3,
                'nCommons':    11
            },
            {
                'name':        'The Dark',
                'packsPerBox': 60,
                'nRares':      0,
                'nUncommons':  2,
                'nCommons':    6
            }
        ]

        print('Inserting old sets...')
        iw = InsertionWrapper()
        for s in sets:
            print('{0}: {1}'.format(s['name'], iw.insertOldSet(s)['message']))

    def buildSetNameMap(self):
        subDir = 'Old cards'
        setNames = ['Antiquities', 'Arabian Nights', 'Fallen Empires', 'Homelands', 'Legends', 'The Dark']
        fileType = 'tsv'

        setNameMap = {}

        try:
            for sn in setNames:
                setNameMap[sn] = {}
                snm = setNameMap[sn]

                # rarityCounts = {}

                fPath = subDir + '/' + sn + '.' + fileType
                with open(fPath, 'r') as f:
                    l = f.readline()
                    while (l):
                        name   = l.split('\t')[0].strip()
                        rarity = l.split('\t')[1].strip()

                        # if (rarity not in rarityCounts):
                        #     rarityCounts[rarity] = 0
                        # rarityCounts[rarity] += 1

                        if (name in snm):
                            print('For set {0}:'.format(sn))
                            print('{0} already in card name map!'.format(name))
                            exit()
                        
                        snm[name] = rarity

                        l = f.readline()

                    # print('\n{0}:'.format(sn))
                    # for r in rarityCounts:
                    #     print('{0}: {1}'.format(r, rarityCounts[r]))

        except Exception as e:
            print(('Could not load file \'{0}\' due to error: \'{1}\'. ' + \
                'Exiting.').format(fPath, str(e)))
            exit(1)

        return setNameMap

        # for sn in setNameMap:
        #     print(sn)
        #     print('-' * len(sn))

        #     cardNameMap = setNameMap[sn]
        #     for cn in cardNameMap:
        #         print('\t{0}: {1}'.format(cn, cardNameMap[cn]))
        #     print('')

    def populateOldCards(self):
        setNameMap = self.buildSetNameMap()

        print('Inserting old sets...')
        iw = InsertionWrapper()

        for sn in setNameMap:
            cardNameMap = setNameMap[sn]

            for cn in cardNameMap:
                rarity = cardNameMap[cn]

                attribs = {
                    'cName':  cn,
                    'sName':  sn,
                    'rarity': rarity
                }

                status = iw.insertOldCard(attribs)
                if (not status['success']):
                    print('Failed to insert {0} (set {1}) because: {2}'.format(cn, sn, status['message']))
