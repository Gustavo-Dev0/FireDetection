from __future__ import print_function
from tabnanny import verbose
from tkinter import *
from tkinter.ttk import Notebook
from turtle import bgcolor
from imutils.video import VideoStream
import time
import cv2
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from client.lbp import compute_lbp
from client.custom_notebook import CustomNotebook
import customtkinter
import glob
import itertools
import os
from keras import models
from keras.applications.imagenet_utils import preprocess_input
from keras.utils import load_img as preprosessing
from keras.utils import img_to_array
import matplotlib.pyplot as plt
import matplotlib.image as imgR
from PIL import Image, ImageOps
import numpy as np

from client.Video import PhotoBoothApp
from client.sobel import Sobel

import os, sys


def resolver_ruta(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath('.'), ruta_relativa)




class TaskFrame(Frame):
    
    def __init__(self, root):
        super().__init__(root)

        root = self
        self.configure(background="black", border=True, borderwidth=2)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=5)


        self.model = models.load_model(resolver_ruta("App/interfaz_app/model/cnn_model_v1.h5"))
        #self.name_entry = ttk.Entry(self)
        #self.name_entry.pack()

        Label(root, text="Analizar:").grid(row=0, column=0, columnspan=3, sticky="nsew")

        boxButtons =  Frame(root)
        boxButtons.columnconfigure(0, weight=1)
        boxButtons.columnconfigure(1, weight=1)
        boxButtons.columnconfigure(2, weight=1)
        boxButtons.rowconfigure(0, weight=1)
        boxButtons.grid(row=1, column=0, columnspan=3, sticky="news")

        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.add_folder_image = self.load_image(resolver_ruta("App/interfaz_app/img/add-folder.png"), 20)
        self.add_list_image = self.load_image(resolver_ruta("App/interfaz_app/img/add-list.png"), 20)

        self.button_1 = customtkinter.CTkButton(master=boxButtons, image=self.add_folder_image, text="Analizar\ncarpeta", height=32,
                                                compound="right", command=self.readImgFolder)
        self.button_1.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.button_2 = customtkinter.CTkButton(master=boxButtons, image=self.add_list_image, text="Analizar\narchivo de imagen", height=32,
                                                compound="right", fg_color="#D35B58", hover_color="#C77C78",command=self.readImgFile)
        self.button_2.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        self.button_3 = customtkinter.CTkButton(master=boxButtons, image=self.add_list_image, text="Analizar\ndesde cámara", height=32,
                                                compound="right", fg_color="#D99B58", hover_color="#C77C78",command=self.openCamera)
        self.button_3.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")


        boxResults = Frame(root)
        boxResults.columnconfigure(2, weight=1)
        boxResults.columnconfigure(0, weight=1)
        boxResults.rowconfigure(0, weight=1)
        boxResults.grid(pady=2, row=2, column=0, columnspan=3, sticky='nsew')

        boxResultsImg = Frame(boxResults)
        boxResultsImg.columnconfigure(0, weight=1)
        boxResultsImg.columnconfigure(1, weight=1)
        boxResultsImg.rowconfigure(1, weight=1)
        boxResultsImg.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.imagePreviewName = Label(boxResultsImg, text="<Nombre de imagen>", font=("Arial", 15), wraplength=500)
        self.imagePreviewName.grid(pady=5, row=0, column=0, columnspan=2)
        self.boxResultsImg = boxResultsImg
        self.imagePreview = Label(boxResultsImg,text="<Imagen>", font=("Arial", 40)).grid( pady=5, row=1, column=0, columnspan=2,sticky='nsew')

        self.backB = customtkinter.CTkButton(master=boxResultsImg, text="Anterior", height=24,
                                                fg_color="#D99B58", hover_color="#C77C78",command=self.readBackFile, state=DISABLED)
        self.backB.grid(row=2, column=0, padx=20, pady=10, sticky="nsew", columnspan=1)

        self.nextB = customtkinter.CTkButton(master=boxResultsImg, text="Siguiente", height=24,
                                                fg_color="#D99B58", hover_color="#C77C78",command=self.readNextFile, state=DISABLED)
        self.nextB.grid(row=2, column=1, padx=20, pady=10, sticky="nsew", columnspan=1)

        self.indexFromFolder = 0
        self.currentImage = None

        boxResultsText = Frame(boxResults)
        boxResultsText.columnconfigure(0, weight=1)
        boxResultsText.columnconfigure(1, weight=1)
        boxResultsText.rowconfigure(1, weight=1)

        boxResultsText.grid(row=0, column=2, columnspan=1, sticky='nsew')

        Label(boxResultsText, text="Resultado:", font=("Arial", 25)).grid(pady=5, row=0, column=0, columnspan=2, sticky='ew', rowspan=1)
        #Label(boxResultsText, text="Resultadow\nefwefwefwef:").grid(pady=5, row=1, column=0, columnspan=1, sticky='nsew', rowspan=8)
        self.textArea = Label(boxResultsText, text="Esperando...", font=("Arial", 40), wraplength=300)
        self.textArea.grid(padx=10, pady=5, row=1, column=0, columnspan=2, sticky='nsew')

        button_grad = customtkinter.CTkButton(master=boxResultsText, text="Ver gradiente", fg_color="#A99B58", hover_color="#C77C78",command=self.run_sobel)
        button_grad.grid(row=2, column=0, padx=20, pady=10, columnspan=1, sticky='nsew',rowspan=1)

        button_lbp = customtkinter.CTkButton(master=boxResultsText, text="Ver LBP", fg_color="#A99B58", hover_color="#C77C78",command=self.run_lbp)
        button_lbp.grid(row=2, column=1, padx=20, pady=10, columnspan=1, sticky='nsew',rowspan=1)



    def readImgFile(self):
        
        filename=filedialog.askopenfilename()     #Obtenga la ruta completa del archivo
        #img=ImageTk.PhotoImage(Image.open(filename))   #tkinter solo puede abrir archivos gif, aquí use la biblioteca PIL
        if not filename:
            print("Error")
            return

        self.analyzeImage(filename)
        return

    def readImgFolder(self):
        
        foldername=filedialog.askdirectory()   

        if not foldername:
            print("Error")
            return
        
        tipos = ('*.jpg', '*.png', '*.jpeg')

        self.imagesFromFolder = [glob.glob(f"{foldername}/{tip}") for tip in tipos]
        self.imagesFromFolder = list(itertools.chain(*self.imagesFromFolder))
        print(self.imagesFromFolder)

        #BUTTONS ACTIVE
        self.indexFromFolder = -1
        self.analyzeImage(self.imagesFromFolder[self.indexFromFolder])
        if(len(self.imagesFromFolder) > 1):
            self.nextB.state = NORMAL
        return

    def readNextFile(self):
        
        
        self.indexFromFolder = self.indexFromFolder + 1 
        self.analyzeImage(self.imagesFromFolder[self.indexFromFolder])

        if(self.indexFromFolder >= len(self.imagesFromFolder)-1):
            self.nextB.state = DISABLED

        if(self.indexFromFolder > 0):
            self.backB.state = NORMAL

    def readBackFile(self):

        self.indexFromFolder = self.indexFromFolder - 1
        self.analyzeImage(self.imagesFromFolder[self.indexFromFolder])

        if(self.indexFromFolder <= 0):
            self.backB.state = DISABLED

        if(self.indexFromFolder < len(self.imagesFromFolder)-1):
            self.nextB.state = NORMAL

    def analyzeImage(self, filename):

        self.img = self.load_image(filename, 200)

        self.imagePreview = Label(self.boxResultsImg, image=self.img)
        self.imagePreview.grid( pady=5, row=1, column=0, columnspan=2,sticky='nsew')
        self.imagePreviewName.config(text = filename)

        #Prediction

        path_image = filename
        #feature = compute_lbp(arr)
        imgToP = preprosessing(path_image, target_size=(224, 224))
        x = img_to_array(imgToP)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)


        prediction = self.model.predict(x)
        print(prediction[0])
        
        if prediction[0][0] > 0.5:
            result = "No se ha detectado fuego"
            self.textArea.configure(text=result, fg='#0f0')
        else:
            result = "Se ha detectado fuego"
            self.textArea.configure(text=result, fg='#f00')
        
        #End Prediction
        self.currentImage = filename
        print(filename)

    def openCamera(self):
        a = PhotoBoothApp(con=self)
        return

    def savePredictioninImage(self):

        if self.currentImage is None:
            return

        f = filedialog.asksaveasfile(initialfile = 'Untitled.txt', defaultextension=".txt",filetypes=[("Text Documents","*.txt")])
        print(f)
        #file = open(f, "w")
        file = f
        toSavePrediction = self.currentImage

        #Prediction

        result = "Resultado de predicicon"

        file.write("Resultado\n")
        file.write("Imagen: "+toSavePrediction+"\n")
        file.write(result)
        file.close()
        return


    def load_image(self, path, image_size):
        return ImageTk.PhotoImage(Image.open("" + path).resize((image_size, image_size)))

    def run_lbp(self):

        if self.currentImage is None:
            return

        img = Image.open(self.currentImage)
        img = img.resize((224, 224), Image.ANTIALIAS)
        if img.mode != 'L':
            img = ImageOps.grayscale(img)
        arr = np.array(img)
        arr = compute_lbp(arr)

    def run_sobel(self):

        if self.currentImage is None:
            return

        img = Image.open(self.currentImage)
        img = img.resize((224, 224), Image.ANTIALIAS)
        arr = np.array(img)
        s = Sobel(img=arr)
        s.gradiente()
        s.show_image()

    def analyzeCamera(self, pathImg):
        print("Hola")
        self.analyzeImage(pathImg)


class MainFrame(Frame):
    def __init__(self, root=None):
        super().__init__(root)

        addButton = customtkinter.CTkButton(master=self, text="Agregar ventana", height=24,fg_color="#D99B58", hover_color="#C77C78",command=self.addTask)
        addButton.pack()


        # Crear el panel de pestañas.

        self.notebook = CustomNotebook(self)
        
        self.greeting_frame = TaskFrame(self.notebook)
        self.notebook.add(
            self.greeting_frame, text="Tarea", padding=10)
        
        self.notebook.pack(padx=5, pady=5, expand=True, fill='both')
        self.pack(expand=True, fill='both')
        self.configure()

    def addTask(self):
        self.greeting_frame = TaskFrame(self.notebook)
        self.notebook.add(
            self.greeting_frame, text="Tarea", padding=10)
