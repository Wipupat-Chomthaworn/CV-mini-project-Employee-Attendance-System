import cv2
import face_recognition
import os
import pandas as pd
import datetime

# Load the list of known faces and their names
known_faces = []
known_names = []

for filename in os.listdir('known_faces'):
    image = face_recognition.load_image_file(os.path.join('known_faces', filename))
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(os.path.splitext(filename)[0])

# Initialize the video capture from the default camera
cap = cv2.VideoCapture(0)

# Create a list to store the detected faces and timestamps
detected_faces = []

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to the grayscale image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Detect the faces in the thresholded image
    face_locations = face_recognition.face_locations(thresh)

    # Loop through the detected faces and compare them to the known faces
    for (top, right, bottom, left) in face_locations:
        face_encoding = face_recognition.face_encodings(thresh, [(top, right, bottom, left)])[0]

        matches = face_recognition.compare_faces(known_faces, face_encoding)

        # Find the best match among the known faces
        best_match_index = matches.index(True) if True in matches else -1

        # Draw a rectangle around the detected face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        if best_match_index >= 0:
            name = known_names[best_match_index]
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Add the detected face and timestamp to the list
            timestamp = datetime.datetime.now()
            detected_faces.append({'Name': name, 'Timestamp': timestamp})

    # Display the resulting image
    cv2.imshow('frame', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()

# Save the detected faces and timestamps to an Excel file
df = pd.DataFrame(detected_faces)
df.to_excel('detected_faces.xlsx', index=False)
