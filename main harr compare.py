import cv2
import numpy as np

# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the reference image and convert it to grayscale
img_ref = cv2.imread('ref_img.jpg')
gray_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2GRAY)

# Detect faces in the reference image
faces_ref = face_cascade.detectMultiScale(gray_ref, scaleFactor=1.1, minNeighbors=5)

# Extract the first face region from the reference image
(x_ref, y_ref, w_ref, h_ref) = faces_ref[0]
face_ref = gray_ref[y_ref:y_ref+h_ref, x_ref:x_ref+w_ref]

# Resize the reference face region to a standard size
face_ref = cv2.resize(face_ref, (100, 100))

# Load the test image and convert it to grayscale
img_test = cv2.imread('test_img.jpg')
gray_test = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)

# Detect faces in the test image
faces_test = face_cascade.detectMultiScale(gray_test, scaleFactor=1.1, minNeighbors=5)

# Extract the first face region from the test image
(x_test, y_test, w_test, h_test) = faces_test[0]
face_test = gray_test[y_test:y_test+h_test, x_test:x_test+w_test]

# Resize the test face region to a standard size
face_test = cv2.resize(face_test, (100, 100))

# Compute the Euclidean distance between the two faces
dist = np.linalg.norm(face_ref - face_test)

# Set a threshold for the distance
threshold = 50

# If the distance is below the threshold, the faces are a match
if dist < threshold:
    print('Faces match!')
else:
    print('Faces do not match.')
