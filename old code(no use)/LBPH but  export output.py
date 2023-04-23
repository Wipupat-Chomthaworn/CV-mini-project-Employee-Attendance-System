import cv2
import os
import numpy as np

# Load the known faces from the 'KnownFaces' folder
known_faces_dir = 'KnownFaces'
known_face_names = []
known_face_images = []
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

# Create a directory to save the exported images
export_dir = 'ExportedFaces'
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

while True:
    # Capture a single frame from the camera
    ret, frame = video_capture.read()

    # Convert the image to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

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
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Export the face ROI as a separate image
        roi_path = os.path.join(export_dir, f'{name}_{confidence:.0f}.jpg')
       
        cv2.imwrite(roi_path, face_roi_gray)
        print("export roi", roi_path)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Exit the program if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()






# import cv2
# import os
# import numpy as np

# # Load the known faces from the 'KnownFaces' folder
# known_faces_dir = 'KnownFaces'
# known_face_names = []
# known_face_images = []
# for dir_name in os.listdir(known_faces_dir):
#     dir_path = os.path.join(known_faces_dir, dir_name)
#     if os.path.isdir(dir_path):
#         images = []
#         for img_name in os.listdir(dir_path):
#             img_path = os.path.join(dir_path, img_name)
#             if os.path.isfile(img_path):
#                 img = cv2.imread(img_path)
#                 img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                 images.append(img)
#         if len(images) > 0:
#             known_face_images.append(images)
#             known_face_names.append(dir_name)
# print("Known faces:", known_face_names)

# # Train the face recognizer
# face_recognizer = cv2.face.LBPHFaceRecognizer_create()
# faces = []
# labels = []
# for i, images in enumerate(known_face_images):
#     for img in images:
#         faces.append(img)
#         labels.append(i)
# face_recognizer.train(faces, np.array(labels))

# # Create a new directory to store the exported ROIs
# export_dir = 'DetectedFaces'
# if not os.path.exists(export_dir):
#     os.makedirs(export_dir)

# # Turn on the camera
# video_capture = cv2.VideoCapture(0)
# while True:
#     # Capture a single frame from the camera
#     ret, frame = video_capture.read()

#     # Convert the image to grayscale
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect faces in the image
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#     # Loop through each face found in the frame and check if it matches a known face
#     for (x, y, w, h) in faces:
#         face_roi_gray = gray_frame[y:y+h, x:x+w]
#         label, confidence = face_recognizer.predict(face_roi_gray)
#         if confidence < 100:
#             name = known_face_names[label]
#         else:
#             name = 'Unknown'

#         # Draw a rectangle around the face
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

#         # Write the name of the person on the rectangle
#         cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
#         # Export the ROI of the detected face to an image file
#         roi_file_path = os.path.join(export_dir, f"{name}_{x}_{y}_{w}_{h}.jpg")
#         roi_img = gray_frame[y:y+h, x:x+w]
#         cv2.imwrite(roi_file_path, roi_img)

#     # Display the resulting image
#     cv2.imshow('Video', frame)

#     # Exit the program if the 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture object and close all windows
# video_capture.release()
# cv2.destroyAllWindows()
