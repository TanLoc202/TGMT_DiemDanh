import sqlite3

# Kết nối đến cơ sở dữ liệu (nếu không tồn tại, sẽ tự động tạo mới)
conn = sqlite3.connect('dbsinhvien.db')

def create_table():
    # Tạo con trỏ
    c = conn.cursor()

    # Tạo bảng dbsinhvien
    c.execute('''CREATE TABLE IF NOT EXISTS sinhvien (
                    Mssv INTEGER PRIMARY KEY,
                    TenSV TEXT NOT NULL,
                    NamSinh INTEGER,
                    NgayTao TEXT DEFAULT CURRENT_TIMESTAMP,
                    NgayCapNhat TEXT DEFAULT CURRENT_TIMESTAMP,
                    SoLanTruyCap INTEGER DEFAULT 0
                )''')

def insert_SV(mssv, tensv, namsinh):
    cur = conn.cursor()
    cur.execute("INSERT INTO sinhvien (Mssv, TenSV, NamSinh) VALUES (?, ?, ?, ?, ?, ?)", (mssv, tensv, namsinh))
    
# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
