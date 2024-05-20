import cv2
from PIL import Image
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
        faceImg = Image.open(img_path).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        faces.append(faceNp)
        labels.append(int(image_name.split('.')[0]))

    # Chuyển đổi danh sách thành mảng NumPy
    labels = np.array(labels)

    # Huấn luyện mô hình
    recognizer.train(faces, labels)

    # Lưu mô hình đã huấn luyện
    recognizer.save('data/face_recognizer.yml')

    print("Model trained and saved successfully.")