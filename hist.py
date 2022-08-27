import cv2
import numpy as np
import matplotlib.pyplot as plt

#Leemos la imagen
A = cv2.imread('fire_dataset/fire_images/fire.1.png')

#La convertimos a scala de grises
img_gray = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)

(n, m) = (img_gray.shape)
i = 0
j = 0
k = 0

#Matriz de 0s para obtener las cantidades de cada color
H = np.zeros((256), dtype=int)

#Loop que calcula la gradiente
while i < n:
        j = i
        while j < m:
            value = img_gray[i][j]
            H[value] = H[value] +1
            j = j+1
        i = i + 1

Intensity = np.arange(0, 256, 1)

plt.bar(Intensity, H, color='maroon', width=0.5)
plt.show()

#mostramos la imagen
cv2.imshow("fuego", img_gray)
cv2.waitKey()

