#https://www.github.com/TanLoc202/TGMT_DiemDanh

import os
from module import nhan_dien, nhap_lieu

if not os.path.exists("data"):
    os.mkdir("data")

if __name__=="__main__":
    os.system("cls")
    print("1. Chạy chương trình nhận diện")
    print("2. Chạy chương trình nhập thông tin")
    print("3. Chạy chương trình nhập khuôn mặt")
    print("4. Chạy chương trình huấn luyện")
    key = int(input("Run>>"))
    if key == 1: 
        nhan_dien.run()
    elif key == 2:
        nhap_lieu.run()
    elif key == 3:
        nhan_dien.nhap_khuon_mat()
    elif key == 4:
        nhan_dien.huan_luyen_model()