import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

#--------
model_path = "data/face_recognizer.yml"
img_folder = "data/images/"
db_path = "data/sinhvien.db"
#--------

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def put_vie_text(img, text, position, color, font_size = 30, font_path = "C:/Windows/Fonts/Arial.ttf",):
    # Convert the OpenCV image to a PIL image
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # Load the font and specify the font size
    font = ImageFont.truetype(font_path, font_size)
    
    # Draw the text on the PIL image
    draw.text(position, text, font=font, fill=color)
    
    # Convert the PIL image back to an OpenCV image
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    return img

def huan_luyen_model(data_path = img_folder, model_path = model_path):
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
    print("Đang huấn luyện mô hình")
    # Huấn luyện mô hình
    recognizer.train(faces, labels)
    # Lưu mô hình đã huấn luyện
    recognizer.save(model_path)

    print(f"Mô hình đã được huấn luyện và lưu vào {model_path}.")

def truy_cap():
    cap = cv2.VideoCapture(0)

    while True:
        # Đọc frame từ camera
        ret, frame = cap.read()
        if not ret:
            break

        # Chuyển frame sang ảnh xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Phát hiện khuôn mặt
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Nhận diện từng khuôn mặt
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(roi_gray)
            
            if confidence < 70:
            # Vẽ khung và hiển thị nhãn
                frame = put_vie_text(frame, f"ID: {label}", (x, y-10), (255, 0, 0))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Hiển thị kết quả
        cv2.imshow('Kết quả nhận diện khuôn mặt', frame)

        # Thoát khi nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng camera và đóng tất cả cửa sổ
    cap.release()
    cv2.destroyAllWindows()


