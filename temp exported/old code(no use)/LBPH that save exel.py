import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime
import time

# Load the known faces from the 'KnownFaces' folder
known_faces_dir = 'KnownFaces'
known_face_names = []
known_face_images = []
last_detected = {}
for dir_name in os.listdir(known_faces_dir):
    dir_path = os.path.join(known_faces_dir, dir_name)
    if os.path.isdir(dir_path):
        images = []
        for img_name in os.listdir(dir_path):
            img_path = os.path.join(dir_path, img_name)
            if os.path.isfile(img_path):
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                images.append(img)
        if len(images) > 0:
            known_face_images.append(images)
            known_face_names.append(dir_name)
print("Known faces:", known_face_names)

# Train the face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
faces = []
labels = []
for i, images in enumerate(known_face_images):
    for img in images:
        faces.append(img)
        labels.append(i)
face_recognizer.train(faces, np.array(labels))



# Turn on the camera
video_capture = cv2.VideoCapture(0)



# Load the attendance Excel file or create a new one if it doesn't exist
filename = 'Attendance.xlsx'
sheet_name = 'Attendance'
if os.path.isfile(filename):
    df = pd.read_excel(filename)
    print("Loaded")
else:
    df = pd.DataFrame(columns=['Name', 'Date', 'Timestamp'])
    # Create a new Excel file or overwrite an existing file
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    print("created xlsx")

while True:
    # Capture a single frame from the camera
    ret, frame = video_capture.read()

    # Convert the image to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(
        gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop through each face found in the frame and check if it matches a known face
    for (x, y, w, h) in faces:
        face_roi_gray = gray_frame[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face_roi_gray)
        if confidence < 100:
            name = known_face_names[label]
        else:
            name = 'Unknown'

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Write the name of the person on the rectangle
        cv2.putText(frame, name, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Add the name and current timestamp to the attendance dataframe
        if name != 'Unknown':
            now = time.time()
        
        # Check if the person was detected within the last 30 seconds
            if name in last_detected and now - last_detected[name] < 30:
                print("Skipping duplicate entry for", name)
            else:
                # Add the name and current timestamp to the attendance dataframe
                last_detected[name] = now
                date = datetime.now().strftime('%Y-%m-%d')
                timestamp = datetime.now().strftime('%H:%M:%S')
                row = {'Name': name, 'Date': date, 'Timestamp': timestamp}
                df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)
                print("Added row to attendance dataframe:", row)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the attendance dataframe to an Excel file
df.to_excel(filename, index=False)
print("saving complete", filename)

video_capture.release()
cv2.destroyAllWindows()
