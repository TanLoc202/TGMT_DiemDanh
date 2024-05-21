from module import database as db

db.conn.execute("""UPDATE sinhvien
SET NgayTao = '2024-05-20 05:31:14'
""")
db.dong_kn()