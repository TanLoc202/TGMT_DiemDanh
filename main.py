import cv2
import os
import db

db.open()
db.create_table_SV()

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
            print(file_path)
            stt += 1
        cv2.waitKey(1)

if __name__=="__main__":
    id = 0
    while id != -1:
        id = input("Mssv: ")
        tensv = input("Ten SV: ")
        namsinh = input("Nam Sinh: ")
        db.insert_SV(id, tensv, namsinh)
        # Tách tên từ chuỗi họ và tên
        tach = tensv.split()
        chupanh(tach[-1], id)