# import the necessary packages
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import customtkinter

class PhotoBoothApp:
    def __init__(self, outputPath="", con=None):
        self.padre = con
        self.frame = None        
        self.outputPath = outputPath
        self.flag1 = 0
        win = tki.Toplevel()

        # Set the size of the window
        win.geometry("700x550")

        win.configure(background="black", border=True, borderwidth=2)
        win.columnconfigure(0, weight=1)
        win.rowconfigure(0, weight=1)
        win.rowconfigure(1, weight=1)

        # Create a Label to capture the Video frames
        self.labelSurface =tki.Label(win)
        self.labelSurface.grid(row=0, column=0)
        self.cap= cv2.VideoCapture(2)

        button = customtkinter.CTkButton(master=win, text="Capturar", fg_color="#A99B58", hover_color="#C77C78",command=self.takeSnapshot)
        button.grid(row=1, column=0, padx=20, pady=10, columnspan=1, sticky='nsew',rowspan=1)

        self.window = win

        self.show_frames()
        win.mainloop()

    def show_frames(self):
        
        # Get the latest frame and convert into Image
        cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        self.frame = cv2image
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image = img)
        self.labelSurface.imgtk = imgtk
        self.labelSurface.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        self.labelSurface.after(20, self.show_frames)


    def takeSnapshot(self):
        # grab the current timestamp and use it to construct the
        # output path
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))
        # save the file
        print(self.frame)
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))
        self.file = p
        self.window.destroy()
        self.onClose()

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.padre.analyzeCamera(self.file)
        #self.stopEvent.set()
        #self.vs.stop()
        #self.root.quit()

