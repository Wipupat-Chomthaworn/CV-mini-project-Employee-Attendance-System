import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

# Create the GUI window
window = tk.Tk()
window.title("Employee Attendance System")

# Open the video capture device
cap = cv2.VideoCapture(0)

# Create the label to display the video feed
image_label = tk.Label(window)
image_label.grid(row=0, column=0)

# Create the label to display the text
text_display = tk.Label(window, text='Employee Attendance System', font=('Arial', 16))
text_display.grid(row=0, column=1, sticky='n')

text_name = tk.Label(window, text="Name : ", font=('Arial', 16))
text_name.grid(row=0, column=1)

text_log = tk.Label(window, text="", font=('Arial', 16))
text_log.grid(row=1, column=0)


global df
log_text = ''
recorded_faces = {}

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

def update_feed():
        # Capture a single frame from the camera
        ret, frame = cap.read()

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
            if name != 'Unknown' and name not in recorded_faces:
                now = datetime.now()
                date = now.strftime('%Y-%m-%d')
                timestamp = now.strftime('%H:%M:%S')
                global df, log_text
                
                row = {'Name': name, 'Date': date, 'Timestamp': timestamp}
                update_text(name, date, timestamp, log_text)
                df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)
                print("Added row to attendance dataframe:", row)

                # Add name to recorded_faces dictionary
                recorded_faces[name] = True

                # Save attendance dataframe to Excel file with a new sheet name
                with pd.ExcelWriter(filename, mode='a') as writer:
                    sheet_num = 1
                    sheet_name_new = sheet_name
                    while sheet_name_new in writer.book.sheetnames:
                        sheet_name_new = sheet_name + str(sheet_num)
                        sheet_num += 1
                    df.to_excel(writer, sheet_name=sheet_name_new, index=False)
                    print("Attendance saved to Excel file.")

            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image_tk = ImageTk.PhotoImage(image)
            image_label.config(image=image_tk)
            image_label.image = image_tk

        # Schedule the next update
        image_label.after(1, update_feed)

        # Display the GUI window
        window.update()

def update_text(name, date, time, log):
    name = name.split("-")
    textName = "Name : " + name[0] + "\nEmployee id : " + name[-1] + '\nTime : ' + time + '\n'
    textLog = date + ": " + name[0] + '-' + name[-1] + ' Time : ' + time + '\n'
    text_name.configure(text=textName, justify="left")
    global log_text
    # if (name == old[-1] or log_text == ""):
        # log_text = log + text
        # text_log.configure(text=log_text)
    # else:
    log_text = log + textLog
    text_log.configure(text=log_text, justify="left")


# Start the video feed update loop
update_feed()

# Start the GUI event loop
window.mainloop()


# Release the video capture device
cap.release()
cv2.destroyAllWindows()


