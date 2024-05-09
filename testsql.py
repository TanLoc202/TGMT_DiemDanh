import db
db.open()
cur = db.conn
cur.execute("select * from sinhvien")

cur.execute("delete FROM sinhvien WHERE Mssv = 110120142")
