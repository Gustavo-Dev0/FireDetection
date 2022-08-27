import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from math import sqrt

class Sobel:
    def __init__(self, path= None, img= None):
        if path != None:
            self.image = mpimg.imread(path)
        else:
            self.image = img
        self.original_img = self.image
        #Se establecen los valores de los kernels
        self.vertical = np.array([[1, 0, -1],[2, 0, -2],[1, 0, -1]])
        self.horizontal = np.array([[1, 2, 1],[0, 0, 0],[-1, -2, -1]])
        print(self.image)

    def cvt2gray(self):
        self.image = np.dot(self.image, [1, 1, 1])//3
        self.image = self.image/255
        print(self.image)

#función que calcula la gradiente
    def gradiente(self):
        self.cvt2gray()
        kernel_w = self.vertical.shape[0]//2
        grad_ = np.zeros(self.image.shape)

        self.image = np.pad(self.image, pad_width= ([kernel_w, ], [kernel_w, ]), 
        mode= 'constant', constant_values= (0, 0))

        #Se recorre la matriz de la imagen para realizar la convolución
        for i in range(kernel_w, self.image.shape[0] - kernel_w):
            for j in range(kernel_w, self.image.shape[1] - kernel_w):
                x = self.image[i - kernel_w: i + kernel_w + 1, j - kernel_w: j + kernel_w + 1]
                x = x.flatten() * self.vertical.flatten()
                sum_x = x.sum()

                y = self.image[i - kernel_w: i + kernel_w + 1, j - kernel_w: j + kernel_w + 1]
                y = y.flatten() * self.horizontal.flatten()
                sum_y = y.sum()
        
                grad_[i - kernel_w][j - kernel_w] = sqrt(sum_x**2 + sum_y**2)
        self.image = grad_
        return self.image

    #Funcion que muestra la imagen
    def show_image(self, orig = 0):
        if orig == 1:
            plt.imshow(self.original_img)
            plt.show()
        if orig == 0:
            for i in range(len(self.image)):
                for j in range(len(self.image[0])):
                    self.image[i][j] = 1 - self.image[i][j] 
            plt.imshow(self.image, cmap= 'gray')
            plt.show()

#Condicional que inicia el script
if __name__ == "__main__":
    img = Sobel("g.jpeg")
    img.gradiente()
    img.show_image()
    
