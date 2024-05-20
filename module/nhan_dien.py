import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def huan_luyen_model(data_path = "data/images/", model_path = "data/face_recognizer.yml"):
    # Khởi tạo các danh sách để lưu trữ hình ảnh và nhãn
    faces = []
    labels = []

    # Đọc dữ liệu và gắn nhãn
    for image_name in os.listdir(data_path):
        img_path = os.path.join(data_path, image_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        labels.append(image_name.split('.')[1])

    # Chuyển đổi danh sách thành mảng NumPy
    faces = np.array(faces)
    labels = np.array(labels)

    # Huấn luyện mô hình
    recognizer.train(faces, labels)

    # Lưu mô hình đã huấn luyện
    recognizer.save('data/face_recognizer.yml')

    print("Model trained and saved successfully.")

def chup_anh(cap, name, code, n = 100, folder = "data/images/"):
    if not os.path.exists(folder):
        os.mkdir(folder)

    face_count = 0
    while face_count < n:
        # Đọc frame từ camera
        ret, frame = cap.read()
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
            face_filename = f'{folder}{name}.{code}.{face_count}.jpg'
            cv2.imwrite(face_filename, face)
            
            face_count += 1
