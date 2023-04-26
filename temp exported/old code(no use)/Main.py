import cv2
import face_recognition
import os

# Load the known faces from the 'KnownFaces' folder
known_faces_dir = 'KnownFaces'
known_face_encodings = []
known_face_names = []
for dir_name in os.listdir(known_faces_dir):
    dir_path = os.path.join(known_faces_dir, dir_name)
    if os.path.isdir(dir_path):
        # Load all the image files in the subdirectory
        face_encodings = []
        for file_name in os.listdir(dir_path):
            if file_name.endswith('.jpg'):
                image = face_recognition.load_image_file(os.path.join(dir_path, file_name))
                # Get the encoding for the first face detected in the image, if any
                face_locations = face_recognition.face_locations(image)
                if len(face_locations) > 0:
                    face_encoding = face_recognition.face_encodings(image, face_locations)[0]
                    face_encodings.append(face_encoding)
        
        if len(face_encodings) == 0:
            # No face was detected in any of the pictures, so skip this person
            print(f"No face detected for {dir_name}")
            continue

        # Append the name and face encodings to the known_face_names and known_face_encodings lists
        known_face_encodings.append(face_encodings)
        known_face_names.append(dir_name)
print("face_encoding",known_face_encodings)
print("face_encoding",known_face_names)
# Turn on the camera
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a single frame from the camera
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face found in the frame and check if it matches a known face
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known face
        name = 'Unknown'
        for i, encodings in enumerate(known_face_encodings):
            for encoding in encodings:
                match = face_recognition.compare_faces([encoding], face_encoding, tolerance=0.9)
                if match[0]:
                    name = known_face_names[i]
                    break
            if name != 'Unknown':
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
