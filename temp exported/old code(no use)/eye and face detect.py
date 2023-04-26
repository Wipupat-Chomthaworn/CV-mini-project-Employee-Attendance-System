import numpy as np 
import cv2 
from matplotlib import pyplot as plt
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
img = cv2.imread('../CV-mini-project-Employee-Attendance-System-/IMG_9480.jpg') 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# find the faces in the image
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2) 
    roi_gray = gray[y:y+h, x:x+w] 
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray) 
    for (ex,ey,ew,eh) in eyes: 
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(10,108,228),2)
cv2.imwrite('human_and_phone_result.jpeg',img)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()