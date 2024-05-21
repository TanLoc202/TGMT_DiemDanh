import os
import pandas as pd
from . import database as db

#----------
imgdir_path = "data/images/"
#----------

def xoa_anh(code, directory = imgdir_path):
    if os.path.exists(directory):
        for image_name in os.listdir(directory):
            if image_name.split('.')[0] == code:
                img_path = os.path.join(directory, image_name)
                os.remove(img_path)  

def nhap_thong_tin():
    mssv = input("MSSV: ")        
    tensv = input("Họ Tên: ")
    namsinh = input("Năm Sinh: ")   
    #chen vao csdl
    if db.them_sinhvien(mssv, tensv, namsinh):
        print("Thêm Thành Công")

def nhap_sinhvien_tu_csv():
    file_path = input("CSV_path: ")
    # Đọc file CSV vào DataFrame
    df = pd.read_csv(file_path)

    # Lặp qua từng dòng và thực hiện hàm db.them_sinhvien(Mssv, TenSV, NamSinh)
    for index, row in df.iterrows():
        Mssv = row['Mssv']
        TenSV = row['TenSV']
        NamSinh = row['NamSinh']
    
        db.them_sinhvien(Mssv, TenSV, NamSinh)
        print(f"Thêm sinh viên: Mã SV = {Mssv}, Tên SV = {TenSV}, Năm sinh = {NamSinh}")
        
def xoa_thong_tin():
    mssv = input("mssv cần xóa : ")
    db.xoa_sinhvien(mssv)
    xoa_anh(mssv) 

def xem_thong_tin():
    print(f"{'MSSV':<10} | {'Họ Tên':<30} | {'NSinh':<5} | {'Ngày tạo':<20} | {'Ngày Cập Nhật':<20} | {'Số lần truy cập':<10}")
    rows = db.ds_sinhvien()
    for row in rows:
       print(f"{row[0]:<10} | {row[1]:<30} | {row[2]:<5} | {row[3]:<20} | {row[4]:<20} | {row[5]:<10}")

def run():
    while True:
        os.system("cls")
        print("=================================================")        
        print("1. Nhập thông tin sinh viên")
        print("2. Nhập sinh viên từ file csv")
        print("3. Xóa thông tin sinh viên")
        print("4. Xem danh sách sinh viên")
        print("0. Thoát")
        chon = input("Chọn thao tác muốn thực hiện: ")
        print("=================================================")
        if chon == "1":
            k = 'y'
            while True:
                print("-------------------------------------------------")
                if k.upper() == "Y":
                    nhap_thong_tin()
                elif k.upper() == "N":
                    break
                k = input("Bạn có muốn nhập tiếp không? (Y/N): ")
        elif chon == "2":
            k = "y"
            while True:
                print("-------------------------------------------------")
                if k.upper() == "Y":
                    nhap_sinhvien_tu_csv()
                elif k.upper() == "N":
                    break
                k = input("Bạn có muốn tiếp tục? (Y/N): ")
        elif chon == "3":
            k = "y"
            while True:
                print("-------------------------------------------------")
                if k.upper() == "Y":
                    xoa_thong_tin()
                elif k.upper() == "N":
                    break
                k = input("Bạn có muốn xóa tiếp không? (Y/N): ")
        elif chon == "4":
            print("-------------------------------------------------")
            print("DANH SACH SINH VIEN")
            xem_thong_tin()
            print("-------------------------------------------------")
            input("Nhấn enter để trở lại")
        elif chon == "0":
            break
        else:
            print("Lựa chọn sai. vui lhong chon lại")
    db.dong_kn()

if __name__=="__main__":
    run()
