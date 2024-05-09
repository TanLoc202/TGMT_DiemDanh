import sqlite3

# Kết nối đến cơ sở dữ liệu (nếu không tồn tại, sẽ tự động tạo mới)
conn = sqlite3.connect('dbsinhvien.db')

# Tạo con trỏ
c = conn.cursor()

# Tạo bảng dbsinhvien
c.execute('''CREATE TABLE IF NOT EXISTS dbsinhvien (
                Masv INTEGER PRIMARY KEY,
                Tensv TEXT NOT NULL,
                Namsinh INTEGER,
                NgayTao TEXT DEFAULT CURRENT_TIMESTAMP,
                NgayCapNhat TEXT DEFAULT CURRENT_TIMESTAMP,
                SoLanTruyCap INTEGER DEFAULT 0
            )''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
