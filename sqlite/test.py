
from database import TableCRUD

tc = TableCRUD()

status = tc.createTables()
print(status['message'])

status = tc.dropTables()
print(status['message'])
