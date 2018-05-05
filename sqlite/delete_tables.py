import sqlite3

deleteCardsTableSQL     = "DROP TABLE Cards"

deleteSetsTableSQL      = "DROP TABLE Sets"

deleteCardInSetTableSQL = "DROP TABLE CardInSet"

conn = sqlite3.connect('card_prices.db')

c = conn.cursor()

try:
    res = c.execute(deleteCardsTableSQL)
    res = c.execute(deleteSetsTableSQL)
    res = c.execute(deleteCardInSetTableSQL)

    print('Successfully deleted tables.')
except Exception as e:
    print('Error deleting tables: ' + str(e))
finally:
    conn.commit()
    conn.close()
