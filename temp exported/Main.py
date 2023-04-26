import cv2
import os

# Load the known faces from the 'KnownFaces' folder
known_faces_dir = 'KnownFaces'
known_face_names = []
known_face_cascades = []
print(os.getcwd() +'/CV-mini-project-Employee-Attendance-System-/' + known_faces_dir)
for dir_name in os.listdir(known_faces_dir):
    dir_path = os.path.join(known_faces_dir, dir_name)
    if os.path.isdir(dir_path):
        cascade_path = 'haarcascade_frontalface_default.xml'
        print('xml model',cascade_path)
        if os.path.isfile(cascade_path):
            cascade_classifier = cv2.CascadeClassifier(cascade_path)
            known_face_cascades.append(cascade_classifier)
            known_face_names.append(dir_name)
        else:
            print(f"No Haar cascade file found for {dir_name}")
print("Known faces:", known_face_names)

# Turn on the camera
video_capture = cv2.VideoCapture(0)
while True:
    # Capture a single frame from the camera
    ret, frame = video_capture.read()

    # Convert the image to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using the cascade classifier
    faces = []
    for cascade in known_face_cascades:
        face_rects = cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in face_rects:
            faces.append((x, y, x+w, y+h))

    # Loop through each face found in the frame and check if it matches a known face
    for (left, top, right, bottom) in faces:
        # Check if the face matches any known face
        name = 'Unknown'
        for i, cascade in enumerate(known_face_cascades):
            face_roi_gray = gray_frame[top:bottom, left:right]
            face_roi_color = frame[top:bottom, left:right]
            match = cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(match) > 0:
                name = known_face_names[i]
                break
        

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Write the name of the person on the rectangle
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
