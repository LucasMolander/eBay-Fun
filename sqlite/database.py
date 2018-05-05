import sqlite3

class InsertionWrapper(object):

    #
    # INSERT INTO statements
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
            if (not hasattr(attributes, ra)):
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
            conn = sqlite3.connect('card_prices.db')

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
        pass

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
            conn = sqlite3.connect('card_prices.db')

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
            conn = sqlite3.connect('card_prices.db')

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
