import sqlite3
import json

class SelectWrapper(object):

    #
    # SELECT statements.
    #
    selectAllSetsSQL = "SELECT * FROM Sets"
    selectAllCardSQL = "SELECT * FROM Cards"

    def __init__(self):
        pass

    def selectAllSets(self):
        ret = {
            'success' : True,
            'message' : 'Successfully selected all sets',
            'data' : None
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.selectAllSetsSQL)
            ret['data'] = c.fetchall()
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to select all sets. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def selectAllCards(self):
        ret = {
            'success' : True,
            'message' : 'Successfully selected all cards',
            'data' : None
        }

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.selectAllCardSQL)
            ret['data'] = c.fetchall()
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to select all cards. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret


class InsertionWrapper(object):

    #
    # INSERT INTO statements.
    #
    insertSetSQL = \
        "INSERT INTO Sets "                                                   + \
        "(name, packsPerBox, pFoil, nMythics, nRares, nUncommons, nCommons) " + \
        "VALUES (?, ?, ?, ?, ?, ?, ?)"

    insertCardSQL = \
        "INSERT INTO Cards "      + \
        "(cName, sName, rarity) " + \
        "VALUES (?, ?, ?)"

    def __init__(self):
        pass

    def insertSet(self, attributes):
        ret = {
            'success' : True,
            'message' : 'Successfully inserted set'
        }

        #
        # Verify that we have the correct arguments.
        #
        requiredAttributes = ['name', 'packsPerBox', \
            'pFoil', 'nMythics', 'nRares', 'nUncommons', 'nCommons']
        missing = []

        for ra in requiredAttributes:
            if (ra not in attributes):
                missing.append(ra)
        
        if (len(missing) > 0):
            ret['success'] = False
            ret['message'] = 'Failed to insert set. ' + \
                'Missing attribute(s) in argument to insertSet(): ' + \
                ', '.join(missing)

            return ret

        # Strip down attributes
        strippedAttrs = []
        for i in range(0, len(requiredAttributes)):
            strippedAttrs.append(attributes[requiredAttributes[i]])

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.insertSetSQL, strippedAttrs)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to insert set. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

    def insertCard(self, attributes):
        ret = {
            'success' : True,
            'message' : 'Successfully inserted card'
        }

        #
        # Verify that we have the correct arguments.
        #
        requiredAttributes = ['cName', 'sName', 'rarity']
        missing = []

        for ra in requiredAttributes:
            if (ra not in attributes):
                missing.append(ra)
        
        if (len(missing) > 0):
            ret['success'] = False
            ret['message'] = 'Failed to insert card. ' + \
                'Missing attribute(s) in argument to insertCard(): ' + \
                ', '.join(missing)

            return ret

        # Strip down attributes
        strippedAttrs = []
        for i in range(0, len(requiredAttributes)):
            strippedAttrs.append(attributes[requiredAttributes[i]])

        try:
            conn = sqlite3.connect('mtg.db')

            c = conn.cursor()
            c.execute(self.insertCardSQL, strippedAttrs)
        except Exception as e:
            ret['success'] = False
            ret['message'] = 'Failed to insert card. Error: ' + str(e)
        finally:
            conn.commit()
            conn.close()

        return ret

class TableCRUD(object):

    #
    # CREATE TABLE statements.
    #
    createSetsTableSQL = \
        "CREATE TABLE Sets ( "               + \
            "name        TEXT PRIMARY KEY, " + \
            "packsPerBox INTEGER, "          + \
            "pFoil       REAL, "             + \
            "nMythics    INTEGER, "          + \
            "nRares      INTEGER, "          + \
            "nUncommons  INTEGER, "          + \
            "nCommons    INTEGER "           + \
        ")"

    createCardsTableSQL = \
        "CREATE TABLE Cards ( "                                                       + \
            "cName  TEXT, "                                                           + \
            "sName  TEXT, "                                                           + \
            "rarity TEXT CHECK(rarity IN ('Mythic', 'Rare', 'Uncommon', 'Common')), " + \
            "PRIMARY KEY (cName, sName), "                                            + \
            "FOREIGN KEY (sName) REFERENCES Sets (name) "                             + \
        ")"

    #
    # DROP TABLE statements.
    #
    deleteSetsTableSQL      = "DROP TABLE Sets"
    deleteCardsTableSQL     = "DROP TABLE Cards"

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
            c.execute(self.createSetsTableSQL)
            c.execute(self.createCardsTableSQL)
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
            c.execute(self.deleteSetsTableSQL)
            c.execute(self.deleteCardsTableSQL)
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
                print('{0} - {1}: {2}. {3}'.format(setName, n, len(cards), rarities))

        
        # weirdos = ['Arabian Nights', 'Fallen Empires', 'Antiquities', 'Homelands', 'The Dark']

        # # print(name)
        # if (name in weirdos):
        #     print('{0}: {1}'.format(name, mtgSet['booster']))

    def loadIntoDB(self):
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


