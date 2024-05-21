model_path = "data/face_encodings.pkl"
imgdir_path = "data/images/"
#-----------------------

import face_recognition
import os
import cv2
import pickle

def huan_luyen(data_path = imgdir_path, model_path = model_path):
    known_encodings = []
    known_names = []

    print('Đang nhập ảnh')
    for filename in os.listdir(data_path):
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
    # Tải mã hóa khuôn mặt và ID từ file
    with open(model, "rb") as f:
        known_face_encodings, known_face_ids = pickle.load(f)

    # Khởi tạo video capture (nếu bạn dùng camera)
    cap = cv2.VideoCapture(camera)

    while True:
        # Lấy frame hiện tại từ video
        ret, frame = cap.read()
        
        # Chuyển đổi frame từ BGR (OpenCV) sang RGB (face_recognition)
        rgb_frame = frame[:, :, ::-1]
        
        # Phát hiện các khuôn mặt trong frame hiện tại
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
        # So sánh từng khuôn mặt trong frame với các mã hóa đã biết
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
        
            # Nếu tìm thấy khớp
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_ids[first_match_index]
            
            face_names.append(name)
    
        # Hiển thị kết quả
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Vẽ hình chữ nhật xung quanh khuôn mặt
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # Vẽ tên người phía dưới khuôn mặt
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # Hiển thị frame kết quả
        cv2.imshow('Video', frame)
        
        # Nhấn 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng video capture và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()
