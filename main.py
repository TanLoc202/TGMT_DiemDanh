import cv2, os, re
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

def find_images_with_key(directory, key):
    image_files = []
    pattern = re.compile(f".*.{key}.*\.(jpg|jpeg|png|gif|bmp)", re.IGNORECASE)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.match(file):
                image_files.append(os.path.join(root, file))
    
    return image_files

def Xoa_Thong_Tin(mssv):
    if db.delete_SV(mssv):
        pass
    else:
        pass

db.open()
db.create_table_SV()

if __name__=="__main__":
    while True:
        Nhap_Thong_Tin()
        print("Bạn có muốn Nhập Tiếp Không? (Y/N)")
        key = input(">>")
        if key == "y" or key =="Y":
            continue
        else: 
            break
    db.save()
    db.close()