import sqlite3



createCardsTableSQL = \
    "CREATE TABLE Cards ( "                                                      + \
        "name   TEXT PRIMARY KEY, "                                              + \
        "rarity TEXT CHECK(rarity IN ('Mythic', 'Rare', 'Uncommon', 'Common')) " + \
    ")"

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

createCardInSetTableSQL = \
    "CREATE TABLE CardInSet ( "                         + \
        "cName TEXT, "                                  + \
        "sName TEXT, "                                  + \
        "PRIMARY KEY(cName, sName), "                   + \
        "FOREIGN KEY (cName) REFERENCES Cards (name), " + \
        "FOREIGN KEY (sName) REFERENCES Sets  (name) "  + \
    ")"

conn = sqlite3.connect('card_prices.db')

c = conn.cursor()
c.execute(createCardsTableSQL)
c.execute(createSetsTableSQL)
c.execute(createCardInSetTableSQL)

conn.commit()
conn.close()
