import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import time
import calendar
from datetime import datetime

# Load the known faces from the 'KnownFaces' folder
known_faces_dir = 'KnownFaces'
known_face_names = []
known_face_cascades = []
print(os.getcwd() + '/CV-mini-project-Employee-Attendance-System-/' + known_faces_dir)
for dir_name in os.listdir(known_faces_dir):
    dir_path = os.path.join(known_faces_dir, dir_name)
    if os.path.isdir(dir_path):
        cascade_path = 'haarcascade_frontalface_default.xml'
        print('xml model', cascade_path)
        if os.path.isfile(cascade_path):
            cascade_classifier = cv2.CascadeClassifier(cascade_path)
            known_face_cascades.append(cascade_classifier)
            known_face_names.append(dir_name)
        else:
            print(f"No Haar cascade file found for {dir_name}")
print("Known faces:", known_face_names)


# name = 'Unknown'
# Define the function to update the video feed


def update_feed():
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to RGB format and resize it
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (640, 480))

# while True:
    # Capture a single frame from the camera
    ret, frame = cap.read()

    # Convert the image to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using the cascade classifier
    faces = []
    for cascade in known_face_cascades:
        face_rects = cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in face_rects:
            faces.append((x, y, x+w, y+h))

    # Loop through each face found in the frame and check if it matches a known face
    print('loop 1 finished')
    for (left, top, right, bottom) in faces:
        # Check if the face matches any known face
        # update_text(name)
        name = 'Unknown'

        best_match_score = 0
        for i, cascade in enumerate(known_face_cascades):
            face_roi_gray = gray_frame[top:bottom, left:right]
            face_roi_color = frame[top:bottom, left:right]
            match = cascade.detectMultiScale(
                face_roi_gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
            print('loop 2 finished')

            if len(match) > 0:
                for (mx, my, mw, mh) in match:
                    # Calculate the match score as the area of the intersection between the detected face and the known face
                    match_area = (min(right, mx+mw) - max(left, mx)) * \
                        (min(bottom, my+mh) - max(top, my))
                    match_score = match_area / \
                        ((right - left) * (bottom - top))

                    # If this match score is better than the previous best score, update the name of the best match
                    if match_score > best_match_score:
                        best_match_score = match_score
                        name = known_face_names[i]

                    update_text(name)

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top),
                            (right, bottom), (0, 0, 255), 2)

            # Write the name of the person on the rectangle
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # Display the resulting image
        # cv2.imshow('Video', frame)

    # Exit the program if the 'q' key is pressed
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break






    # text_display.configure(text=name)



    # Convert the frame to a PIL image and display it in the label

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    image = Image.fromarray(frame)
    image_tk = ImageTk.PhotoImage(image)
    image_label.configure(image=image_tk)
    image_label.image = image_tk

    # Schedule the next update
    image_label.after(10, update_feed)



def update_text(new):
    print(new)
    old = text_display.cget("text")
    # if old == new:
    #     text = new
    # if len(old) > 10:
    #     old = old.split('\n')[-1]
    timestamp = time.time()
    dt_object = datetime.fromtimestamp(timestamp)

    dt_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    print("Current timestamp:", dt_string)
    text = "Name : " + new + " time : " + dt_string
    text_display.configure(text=text)


# Create the GUI window
window = tk.Tk()
window.title("GUI")


# Create the label to display the video feed
image_label = tk.Label(window)
image_label.grid(row=0, column=0)

# Create the label to display the text
text_display = tk.Label(window, text='texttextext', font=('Arial', 16))
text_display.grid(row=0, column=1, sticky='n')

# # Create the input field for text
# text_input = tk.Entry(window, font=('Arial', 16))
# text_input.pack()

text_display = tk.Label(window, text="asdf")
text_display.grid(row=0, column=1)


# Open the video capture device
cap = cv2.VideoCapture(0)

# Start the video feed update loop
update_feed()

# Start the GUI event loop
window.mainloop()

# Release the video capture device
cap.release()
