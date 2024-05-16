import cv2
import numpy as np

# Kiểm tra xem module cv2.face có tồn tại hay không
if not hasattr(cv2, 'face'):
    raise Exception("Module 'cv2.face' không tồn tại. Hãy cài đặt 'opencv-contrib-python' bằng lệnh 'pip install opencv-contrib-python'.")

# Load the trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('model/training.yml')

# Load prebuilt model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize and start the video frame capture from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        
        # Recognize the face
        Mssv, confidence = recognizer.predict(roi_gray)
        
        # Check if confidence is less than 100 (0 is perfect match)
        if confidence < 80:
            text = f"ID: {Mssv}, \n {round(100 - confidence)}%"
        else:
            text = "Unknown"

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Display the label with the name and confidence
        cv2.putText(frame, text, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Press 'q' to exit the video window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
