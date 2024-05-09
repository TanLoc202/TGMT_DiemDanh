import cv2
import os
import db


def chupanh(name, code):
    if not os.path.exists("images"):
        os.mkdir("images")

    camera = cv2.VideoCapture(0)
    stt = 1
    while camera.isOpened() and stt <21:
        ret, frame = camera.read()
        if not ret:
            print("Không thể đọc frame từ webcam.")
            break
        else:
            file_path = f'images/{name}.{code}.{stt}.jpg'
            cv2.imwrite(file_path, frame)
            stt += 1
        cv2.waitKey(1)

def Nhap_Thong_Tin():
    print("====================================================================")
    mssv = input("Mssv: ")    
    # Kiểm tra xem id đã tồn tại trong cơ sở dữ liệu hay chưa
    if db.check_id_exist(mssv):
        print("Sinh Vien Đã Tồn Tại.")
        return      
    tensv = input("Ten SV: ")
    namsinh = input("Nam Sinh: ")
        
    #chen vao csdl
    if db.insert_SV(mssv, tensv, namsinh):
        print("Đang chụp ảnh")
        ten = tensv.split()[-1]
        chupanh(ten, mssv)
        print("Đã chụp ảnh")

db.open()
db.create_table_SV()

if __name__=="__main__":
    while True:
        Nhap_Thong_Tin()
    db.save()
    db.close()
