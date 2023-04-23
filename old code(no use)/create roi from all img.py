import cv2
import os
import numpy as np

# Define the paths for the input and output directories
known_faces_dir = 'KnownFaces'
known_faces_roi_dir = 'KnownFaces_ROIs'

# Create a new directory for the ROIs if it doesn't exist
if not os.path.exists(known_faces_roi_dir):
    os.makedirs(known_faces_roi_dir)

# Load the known faces from the 'KnownFaces' folder
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

# Export the face ROIs as separate image files
for i, images in enumerate(known_face_images):
    for j, img in enumerate(images):
        roi_path = os.path.join(known_faces_roi_dir, f'{known_face_names[i]}_{j}.jpg')
        cv2.imwrite(roi_path, img)
