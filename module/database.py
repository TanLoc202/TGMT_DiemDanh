import sqlite3
from datetime import datetime

conn = None

def mo_kn(filedb='data/sinhvien.db'):
    global conn
    conn = sqlite3.connect(filedb)
    tao_bang_sinhvien()
    tao_bang_diemdanh()

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

def tao_bang_diemdanh():
    try:
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS diemdanh (
                                Mssv INTEGER,
                                Ngay TEXT,
                                FOREIGN KEY (Mssv) REFERENCES sinhvien (Mssv),
                                PRIMARY KEY (Mssv, Ngay)
                            )''')
    except sqlite3.Error as e:
        print("SQLite - Lỗi khi tạo bảng check_in", e)

def kiem_tra_sinhvien(mssv):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sinhvien WHERE Mssv = ?", (mssv,))
    return cur.fetchone()[0] > 0

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

def xoa_sinhvien(mssv):
    cur = conn.cursor()
    cur.execute("DELETE FROM diemdanh WHERE Mssv = ?", (mssv,))
    cur.execute("DELETE FROM sinhvien WHERE Mssv = ?", (mssv,))
    return cur.rowcount > 0

def ds_sinhvien(dieukien = ""):
    cur = conn.cursor()
    sql = "SELECT * FROM sinhvien"
    if dieukien != "":
        sql += f" where {dieukien}"
    cur.execute(sql)
    return cur.fetchall()

def kiem_tra_truy_cap(mssv, ngay):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM diemdanh WHERE Mssv = ? and Ngay = ?", (mssv, ngay))
    return cur.fetchone()[0] > 0

def truy_cap(mssv):
    current_date = datetime.now().date()
    if not kiem_tra_truy_cap(mssv, current_date):
        try:
            with conn:
                conn.execute("INSERT INTO diemdanh (Mssv, Ngay) VALUES (?, ?)", (mssv, current_date))
                conn.execute("UPDATE sinhvien SET SoLanTruyCap = SoLanTruyCap + 1, NgayCapNhat = CURRENT_TIMESTAMP WHERE Mssv = ?", (mssv,))
                return True
        except sqlite3.Error as e:
            print("SQLite - Lỗi khi chèn dữ liệu:", e)
            return False

def diemdanh_ngay(ngay):
    cur = conn.cursor()
    sql = """SELECT DISTINCT
    sinhvien.Mssv,
    sinhvien.TenSV,
    sinhvien.NamSinh,
    CASE
        WHEN sinhvien.mssv in (SELECT DISTINCT diemdanh.Mssv
FROM diemdanh
WHERE diemdanh.Ngay = ?) THEN 1
        ELSE 0
    END AS DiemDanh
FROM sinhvien;"""
    cur.execute(sql, (ngay,))
    return cur.fetchall()      

def dong_kn():
    conn.close()

mo_kn()