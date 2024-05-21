#--------
model_path = "data/face_recognizer.yml"
imgdir_path = "data/images/"
#--------

import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from . import database as db
from datetime import datetime
from openpyxl import Workbook

import tkinter as tk
from tkinter import simpledialog    
root = tk.Tk()
root.withdraw()  # Ẩn cửa sổ chính

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def nhap_khuon_mat(camera = 0, directory = imgdir_path):
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    cap = cv2.VideoCapture(camera)
    X, Y, W, H = 200, 100, 250, 250
    count = 100
    while True:
        # Đọc frame từ camera
        ret, frame = cap.read()
        if not ret:
            break

        key = cv2.waitKey(1)
        # Thoát khi nhấn phím 'q'
        if key == ord('q'):
            break
        elif key == ord('p'):
            mssv = simpledialog.askstring("Nhập MSSV", "Nhập mã số sinh viên")
            count = 0

        if count == 100:
            frame = put_vie_text(frame, "Nhấn P để nhập khuôn mặt mới", (200, 100), (255, 255, 255), 20)
            cv2.imshow('Nhap Khuon Mat', frame)
            continue

        # Chuyển frame sang ảnh xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Phát hiện khuôn mặt
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        text = "Đưa khuôn mặt vào đây"
        color = (0, 0, 255)
        # Nhận diện từng khuôn mặt
        for (x, y, w, h) in faces:            
            if x > X and y > Y and x+w < X+W and y+h < Y+H:
                if x < X+60 and y < Y+60 and x+w > X+W-60 and y+h > Y+H-60:
                    text = "Giữ Cố Định"
                    color = (20, 200, 20)
                    cv2.imwrite(f"{directory}{mssv}.{count}.jpg", frame[Y:Y+H, X:X+W])
                    count += 1
                    cv2.rectangle(frame, (X, Y+H), (X+W, Y+H+30), color, -1)
                    frame = put_vie_text(frame, f"- {count}/100 -", (X+5, Y+W+5), (255, 255, 255), 20)
                else: 
                    text = "Gần thêm chút"

        cv2.rectangle(frame, (X, Y-30), (X+W, Y), color, -1)
        cv2.rectangle(frame, (X, Y), (X+W, Y+H), color, 2)
        frame = put_vie_text(frame, text, (X+5, Y-25), (255, 255, 255), 20)

        # Hiển thị kết quả
        cv2.imshow('Nhap Khuon Mat', frame)

    # Giải phóng camera và đóng tất cả cửa sổ
    cap.release()
    cv2.destroyAllWindows()

def huan_luyen_model(data_path = imgdir_path, model_path = model_path):
    if os.path.exists(data_path):
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
        
        if labels != []:
            # Chuyển đổi danh sách thành mảng NumPy
            labels = np.array(labels)
            print("Đang huấn luyện mô hình")
            recognizer.train(faces, labels)
            recognizer.save(model_path)
            print(f"Mô hình đã được huấn luyện và lưu vào {model_path}.")
        else:
            print("Không tìm thấy dữ liệu để huấn luyện")
    else:
        print("Đường dẫn đến thư mực chứa dữ liệu huấn luyện không tồn tại")

def put_vie_text(img, text, position, color, font_size = 30, font_path = "C:/Windows/Fonts/Arial.ttf",):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    return img

def xuat_file_diemdanh_ngay(ngay, file_path=""):
    rows = db.diemdanh_ngay(ngay)
    rows = [[f"DANH SACH DIEM DANH NGAY {ngay}"], ["MSSV", "Họ Tên", "Năm Sinh", "Diem Danh"]] + rows
    # Khởi tạo một workbook và Tạo một worksheet mới
    wb = Workbook()
    ws = wb.active
    
    for row_index, row_data in enumerate(rows, start=1):
        for col_index, cell_value in enumerate(row_data, start=1):
            ws.cell(row=row_index, column=col_index, value=cell_value)
    # Lưu workbook vào file Excel
    if file_path == "":
        file_path = f"diemdanh_{ngay}.xlsx"
    wb.save(file_path)

def run(camera = 0):
    recognizer.read(model_path)
    cap = cv2.VideoCapture(camera)
    oid = 0
    cid = 0
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
            color = (255, 0, 0)
            roi_gray = gray[y:y+h, x:x+w]
            id, confidence = recognizer.predict(roi_gray)
            if confidence < 60:
            # Vẽ khung và hiển thị nhãn
                text = f"ID: {id}"
                
                if oid == id:
                    cid +=1
                else:
                    oid = id
                    cid = 0
                if cid == 5:
                    color = (0, 200, 0)
                    db.truy_cap(id)
            else: 
                text = f"Không Xác Định"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)         
            cv2.rectangle(frame, (x, y-20), (x+w, y), color, -1)
            frame = put_vie_text(frame, text, (x, y-20), (255, 255, 255),20)
        # Hiển thị kết quả
        cv2.imshow('Nhan Dien Khuon Mat', frame)

        key = cv2.waitKey(1)
        # Thoát khi nhấn phím 'q'
        if key == ord('q'):
            break
        elif key == ord('p'):
            xuat_file_diemdanh_ngay(datetime.now().date())

    # Giải phóng camera và đóng tất cả cửa sổ
    cap.release()
    cv2.destroyAllWindows()
    db.dong_kn()
