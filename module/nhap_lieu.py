import cv2, os, re
from . import ket_noi as db

# Sử dụng bộ phát hiện khuôn mặt Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def chup_anh(camera, code, n = 100, folder = "data/images/"):
    if not os.path.exists(folder):
        os.mkdir(folder)

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
        
        if len(faces) > 0:
            # Lấy khuôn mặt đầu tiên được phát hiện
            (x, y, w, h) = faces[0]
            
            # Vẽ hình chữ nhật xung quanh khuôn mặt
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Cắt vùng chứa khuôn mặt
            face = frame[y:y+h, x:x+w]
            
            # Lưu ảnh khuôn mặt
            face_filename = f'{folder}{code}.{face_count}.jpg'
            cv2.imwrite(face_filename, face)
            
            face_count += 1

def xoa_anh(directory, key):
    pattern = re.compile(f".*{key}.*\.(jpg|jpeg|png|gif|bmp)", re.IGNORECASE)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)  # Xóa file
                    print(f"Đã xóa file: {file_path}")
                except OSError as e:
                    print(f"Lỗi xóa file: {file_path} - {e}")
    
def nhap_thong_tin():
    mssv = input("MSSV: ")        
    tensv = input("Họ Tên: ")
    namsinh = input("Năm Sinh: ")
        
    #chen vao csdl
    if db.them_sinhvien(mssv, tensv, namsinh):
        print("- Chụp Ảnh -")
        chup_anh(cap, mssv)

def xoa_thong_tin(mssv):
    db.xoa_sinhvien(mssv)
    print("- Xóa Ảnh -")
    xoa_anh("images", mssv) 

db.mo_kn()

def run():
    while True:
        print("=================================================")        
        print("1. Nhập Thông Tin Sinh Viên")
        print("2. Xóa Thông Tin Sinh Viên")
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
                    mssv = input("mssv cần xóa : ")
                    xoa_thong_tin(mssv)
                elif k.upper() == "N":
                    break
                k = input("Bạn có muốn xóa tiếp không? (Y/N): ")
        elif chon == "0":
            break
        else:
            print("Lựa chọn sai. vui lhong chon lại")
    db.dong_kn()

if __name__=="__main__":
    run()