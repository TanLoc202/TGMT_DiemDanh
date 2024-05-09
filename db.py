import sqlite3

conn = None

def open(name='dbsinhvien.db'):
    global conn
    conn = sqlite3.connect(name)

def create_table_SV():
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
        print("Lỗi khi tạo bảng:", e)

def insert_SV(mssv, tensv, namsinh):
    try:
        with conn:
            conn.execute("INSERT INTO sinhvien (Mssv, TenSV, NamSinh) VALUES (?, ?, ?)", (mssv, tensv, namsinh))
    except sqlite3.Error as e:
        print("Lỗi khi chèn dữ liệu:", e)

def check_id_exist(mssv):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sinhvien WHERE Mssv = ?", (mssv,))
    count = cur.fetchone()[0]
    return count > 0

def save():
    try:
        conn.commit()
    except sqlite3.Error as e:
        print("Lỗi khi lưu thay đổi:", e)

def close():
    conn.close()
