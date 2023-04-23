import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import shutil
from datetime import datetime

# Function to browse and select a folder
def browse_folder():
    folder_path = filedialog.askdirectory(initialdir="KnownFaces")
    if folder_path:
        # Display the selected folder in the label
        display_selected_folder(folder_path)

# Function to display the selected folder in the label
def display_selected_folder(folder_path):
    global selected_folder_path
    selected_folder_path = folder_path
    folder_label.config(text=f"Selected Folder: {folder_path}")

# Function to confirm and upload the image
def confirm_upload():
    global selected_folder_path
    global uploaded_image_path
    if selected_folder_path and uploaded_image_path:
        filename = os.path.basename(uploaded_image_path)
        destination = os.path.join(selected_folder_path, filename)
        shutil.copy(uploaded_image_path, destination)
        status_label.config(text=f"Image uploaded to '{selected_folder_path}'.")
        selected_folder_path = None
        uploaded_image_path = None
        folder_label.config(text="")
        label.config(image=None)

# Function to browse and upload an image
def browse_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Display the uploaded image in a label
        display_uploaded_image(file_path)

# Function to display the uploaded image in the label
def display_uploaded_image(file_path):
    global uploaded_image_path
    uploaded_image_path = file_path
    image = Image.open(file_path)
    # Display the uploaded image in a label
    image = image.resize((300, 300))  # Resize the image to fit in the label
    image = ImageTk.PhotoImage(image)
    label.config(image=image)
    label.image = image  # Keep a reference to the image to avoid garbage collection

# Global variables to store the selected folder and uploaded image path
selected_folder_path = None
uploaded_image_path = None

# Create the main window
uploadGUI = tk.Tk()
uploadGUI.title("Image Uploader")

# Create labels, buttons, and entry widgets
folder_button = tk.Button(uploadGUI, text="Select Folder", command=browse_folder)
folder_button.pack()

folder_label = tk.Label(uploadGUI, text="")
folder_label.pack()

browse_button = tk.Button(uploadGUI, text="Browse Image", command=browse_image)
browse_button.pack()

confirm_button = tk.Button(uploadGUI, text="Confirm Upload", command=confirm_upload)
confirm_button.pack()

label = tk.Label(uploadGUI)
label.pack()

status_label = tk.Label(uploadGUI, text="")
status_label.pack()

uploadGUI.mainloop()
