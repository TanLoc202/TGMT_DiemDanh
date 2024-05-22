model_path = "data/face_encodings.pkl"
imgdir_path = "data/images/"
#-----------------------

import face_recognition
import os
import cv2
import pickle
from.sp import put_vie_text

def huan_luyen(data_path = imgdir_path, model_path = model_path):
    known_encodings = []
    known_names = []

    print('Đang nhập ảnh')
    for filename in os.listdir(data_path):
        if int(filename.split(".")[1]) % 40 != 0:#---------------------------------------
            continue
        image_path = os.path.join(data_path, filename)
        # Đọc ảnh
        image = face_recognition.load_image_file(image_path)
        # Mã hóa khuôn mặt
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 0:
            encoding = encodings[0]
            known_encodings.append(encoding)
            known_names.append(filename.split('.')[0])

    # Lưu các mã hóa và tên vào file
    with open(model_path, 'wb') as f:
        pickle.dump((known_encodings, known_names), f)

def run(camera = 0, model = model_path):
    print("Đang tải dữ liệu")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Tải mã hóa khuôn mặt và ID từ file
    with open(model, "rb") as f:
        known_face_encodings, known_face_ids = pickle.load(f)

    # Khởi tạo video capture (nếu bạn dùng camera)
    cap = cv2.VideoCapture(camera)

    while True:
        # Lấy frame hiện tại từ video
        ret, frame = cap.read()
        
        # Chuyển đổi frame từ BGR (OpenCV) sang RGB (face_recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Phát hiện các khuôn mặt trong frame hiện tại
        faces = face_cascade.detectMultiScale(rgb_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # Nhận diện từng khuôn mặt
        for (x, y, w, h) in faces: 
            face = rgb_frame[y:y+h, x:x+w]
            face_encoding = face_recognition.face_encodings(face)
            if len(face_encoding) > 0:
        # So sánh từng khuôn mặt trong frame với các mã hóa đã biết
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
                name = "Unknown"
            
                # Nếu tìm thấy khớp
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_ids[first_match_index]
        
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)         
                cv2.rectangle(frame, (x, y-20), (x+w, y), (255, 0, 0), -1)
                frame = put_vie_text(frame, name, (x, y-20), (255, 255, 255),20)

        # Hiển thị frame kết quả
        cv2.imshow('Video', frame)
        
        # Nhấn 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng video capture và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()
