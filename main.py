#https://www.github.com/TanLoc202/TGMT_DiemDanh

img_path = "data/images/"

import os
from module import nhan_dien, nhap_lieu
if not os.path.exists("data"):
    os.mkdir("data")
if not os.path.exists(img_path):
    os.mkdir(img_path)

if __name__=="__main__":
    print("1. Chạy chương trình nhận diện")
    print("2. Chạy chương trình nhập liệu")
    print("3. Chạy chương trình huấn luyện")
    key = int(input("Run>>"))
    if key == 1: 
        nhan_dien.diem_danh()
    elif key == 2:
        nhap_lieu.run()
    elif key == 3:
        nhan_dien.huan_luyen_model()