import os
from module import database as db 
# Đường dẫn thư mục chứa các file

folder_path = 'data/images/'
# Đọc dữ liệu và gắn nhãn
for image_name in os.listdir(folder_path):
    db.truy_cap(int(image_name.split('.')[0]))
 