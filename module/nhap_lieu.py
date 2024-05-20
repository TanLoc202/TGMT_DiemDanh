import cv2, os
from . import database as db
#----------
img_folder = "data/images/"
db_path = "data/sinhvien.db"
#----------

# Sử dụng bộ phát hiện khuôn mặt Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def chup_anh(camera, code, n = 100, directory = img_folder):
    if not os.path.exists(directory):
        os.mkdir(directory)

    face_count = 0
    while face_count < n:
        # Đọc frame từ camera
        ret, frame = camera.read()
        if not ret:
            break
        
        # Chuyển frame sang ảnh xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Phát hiện khuôn mặt
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
        for (x, y, w, h) in faces:
            # Vẽ hình chữ nhật xung quanh khuôn mặt
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Cắt vùng chứa khuôn mặt
            face = frame[y:y+h, x:x+w]
            
            # Lưu ảnh khuôn mặt
            face_filename = f'{directory}{code}.{face_count}.jpg'
            cv2.imwrite(face_filename, face)
            
            face_count += 1

def xoa_anh(code, directory = img_folder):
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
        print("- Đang chụp Ảnh -")
        chup_anh(cap, mssv)

def xoa_thong_tin():
    mssv = input("mssv cần xóa : ")
    db.xoa_sinhvien(mssv)
    print("- Đang xóa Ảnh -")
    xoa_anh(mssv) 

def xem_thong_tin():
    print(f"{'MSSV':<10} | {'Họ Tên':<30} | {'NSinh':<5} | {'Ngày tạo':<20} | {'Ngày Cập Nhật':<20} | {'Số lần truy cập':<10}")
    rows = db.ds_sinhvien()
    for row in rows:
       print(f"{row[0]:<10} | {row[1]:<30} | {row[2]:<5} | {row[3]:<20} | {row[4]:<20} | {row[5]:<10}")

def run():
    while True:
        print("=================================================")        
        print("1. Nhập thông tin Sinh viên")
        print("2. Xóa thông tin Sinh viên")
        print("3. Xem danh sách Sinh viên")
        print("0. Thoát")
        chon = input("Chọn thao tác muốn thực hiện: ")
        print("=================================================")
        if chon == "1":
            print("Đang mở camera")
            
            global cap
            cap = cv2.VideoCapture(0)

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
                    xoa_thong_tin()
                elif k.upper() == "N":
                    break
                k = input("Bạn có muốn xóa tiếp không? (Y/N): ")
        elif chon == "3":
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