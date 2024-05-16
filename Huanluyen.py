import cv2
import os
import numpy as np
from PIL import Image

# Kiểm tra xem module cv2.face có tồn tại hay không
if not hasattr(cv2, 'face'):
    raise Exception("Module 'cv2.face' không tồn tại. Hãy cài đặt 'opencv-contrib-python' bằng lệnh 'pip install opencv-contrib-python'.")

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'images'

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    faces = []
    Mssv = []

    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        # Split to get ID of the image
        Masv = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print(Masv)
        Mssv.append(Masv)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)

    return Mssv, faces

Mssv, faces = getImagesAndLabels(path)

# Training
recognizer.train(faces, np.array(Mssv))
recognizer.save('model/training.yml')
cv2.destroyAllWindows()
