import sqlite3 as sq
con = sq.connect(r'C:\1862\geekshop\db.sqlite3')
cur = con.cursor()
print(sq.Row.keys(cur))
print(sq.PARSE_COLNAMES.conjugate())