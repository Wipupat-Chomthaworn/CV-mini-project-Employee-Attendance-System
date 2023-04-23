import cv2
import os
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

# Create the root window
root = tk.Tk()

# Set the window title
root.title("Employee Attendance System")

# Set the window size
root.geometry("800x600")

# Create the video capture object
camera = cv2.VideoCapture(0)

# Create the image label
image_label = tk.Label(root)
image_label.pack()

# Create the employee name entry box
name_entry = tk.Entry(root)
name_entry.pack()

# Create the employee ID entry box
id_entry = tk.Entry(root)
id_entry.pack()

# Define the function to save the employee image
def save_image():
    # Get the employee name and ID
    name = name_entry.get()
    id = id_entry.get()

    # Create the directory for the employee if it doesn't exist
    if not os.path.exists(f"KnownFaces/{name}-{id}"):
        os.makedirs(f"KnownFaces/{name}-{id}")

    # Save the image
    img_name = f"{name}-{id}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg"
    cv2.imwrite(f"KnownFaces/{name}-{id}/{img_name}", roi)

# Define the function to capture and display the video stream
def show_video_stream():
    # Read a single frame from the camera
    ret, frame = camera.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw a rectangle around each face and save the ROI
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi = frame[y:y+h, x:x+w]
        save_image_button = tk.Button(root, text="Save Image", command=save_image)
        save_image_button.pack()

    # Convert the frame to an image and display it in the window
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

    # Schedule the next update of the video stream
    root.after(10, show_video_stream)

# Load the face cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Start the video stream
show_video_stream()

# Start the main event loop
root.mainloop()

# Release the camera
camera.release()
cv2.destroyAllWindows()
