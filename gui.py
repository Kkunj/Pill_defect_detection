import serial
import time
import tkinter as tk
from tkinter import Label, Button, PhotoImage
from PIL import Image, ImageTk
from inspect4 import NumberOfPills
import cv2
import numpy as np

class PillCounterApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Pill Counter App")

        # Serial port setup
        self.ser = serial.Serial('COM7', 9600)  # Update 'COM3' with the correct serial port on your system

        # GUI elements
        self.label_status = Label(root, text="Waiting for signal...", font=("Helvetica", 16))
        self.label_status.pack(pady=10)

        self.label_original_image = Label(root)
        self.label_original_image.pack(pady=10)

        self.label_processed_image = Label(root)
        self.label_processed_image.pack(pady=10)

        self.label_pill_count = Label(root, text="Number of Pills: 0", font=("Helvetica", 14))
        self.label_pill_count.pack(pady=10)

        self.btn_start = Button(root, text="Start", command=self.start_capture)
        self.btn_start.pack(pady=10)

        self.btn_stop = Button(root, text="Stop", command=self.stop_capture)
        self.btn_stop.pack(pady=10)

        # Flag to indicate whether the process should continue
        self.running = False

    def start_capture(self):
        # Set the flag to continue the process
        self.running = True
        while self.running:
            line = self.ser.readline().decode('utf-8').strip()
            print(line)

            if line == "1":
                print("here")
                count, original_image, processed_image = NumberOfPills()  # Find number of pills and get images
                flag = 1
                # Resize the images
                original_image = cv2.resize(original_image, (300, 300))
                processed_image = cv2.resize(processed_image, (300, 300))

                # Convert the images to PhotoImage format
                original_image_tk = self.convert_image_to_tk(original_image)
                processed_image_tk = self.convert_image_to_tk(processed_image)

                # Update the labels
                self.label_original_image.config(image=original_image_tk)
                self.label_original_image.image = original_image_tk

                self.label_processed_image.config(image=processed_image_tk)
                self.label_processed_image.image = processed_image_tk

                # Update the pill count label
                self.label_pill_count.config(text=f"Number of Pills: {count}")

                # Wait for a short time to avoid high CPU usage
                self.root.update()
                time.sleep(0.1)

    def stop_capture(self):
        # Set the flag to stop the process
        self.running = False

    def convert_image_to_tk(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img)
        return img_tk

    def on_closing(self):
        # Close the serial port when closing the application
        self.running = False  # Stop scheduling the functions
        self.ser.close()
        self.root.destroy()

if __name__ == "_main_":
    root = tk.Tk()
    app = PillCounterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle window close event
    root.mainloop()