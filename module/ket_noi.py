import sqlite3

conn = None

def mo_kn(filedb='data/sinhvien.db'):
    global conn
    conn = sqlite3.connect(filedb)
    # tạo bảng nếu không tồn tại.
    tao_bang_sinhvien()

def tao_bang_sinhvien():
    try:
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS sinhvien (
                                Mssv INTEGER PRIMARY KEY,
                                TenSV TEXT NOT NULL,
                                NamSinh INTEGER,
                                NgayTao TEXT DEFAULT CURRENT_TIMESTAMP,
                                NgayCapNhat TEXT DEFAULT CURRENT_TIMESTAMP,
                                SoLanTruyCap INTEGER DEFAULT 0
                            )''')
    except sqlite3.Error as e:
        print("SQLite - Lỗi khi tạo bảng sinhvien", e)

def them_sinhvien(mssv, tensv, namsinh):
    if not kiem_tra_sinhvien(mssv):
        try:
            with conn:
                conn.execute("INSERT INTO sinhvien (Mssv, TenSV, NamSinh) VALUES (?, ?, ?)", (mssv, tensv, namsinh))
                return True
        except sqlite3.Error as e:
            print("SQLite - Lỗi khi chèn dữ liệu:", e)
            return False
    else:
        print("Sinh Viên đã tồn tại")
        return False

def kiem_tra_sinhvien(mssv):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sinhvien WHERE Mssv = ?", (mssv,))
    return cur.fetchone()[0] > 0

def xoa_sinhvien(mssv):
    cur = conn.cursor()
    cur.execute("DELETE FROM sinhvien WHERE Mssv = ?", (mssv,))
    return cur.rowcount > 0

def ds_sinhvien(dieukien = ""):
    cur = conn.cursor()
    sql = "SELECT * FROM sinhvien"
    if dieukien != "":
        sql += f" where {dieukien}"
    cur.execute(sql)
    return cur.fetchall()

def dong_kn():
    conn.close()