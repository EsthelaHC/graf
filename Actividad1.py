import cv2 as cv
import numpy as np
import math

# Cargar la imagen
img =cv.imread(r"hongos.jpg",0)

# Dimensiones de la imagen
x, y = img.shape[0], img.shape[1]

# Rotación
angle = 60
theta = math.radians(angle)
rotation_matrix = cv.getRotationMatrix2D((y // 2, x // 2), angle, 1)
rotated_img = cv.warpAffine(img, rotation_matrix, (y, x))

# Traslación
tx, ty = 10, 10  # Cambia estos valores según tu requerimiento
translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
translated_img = cv.warpAffine(rotated_img, translation_matrix, (y, x))

# Escalado
scale_factor = 1/5
scaled_img = cv.resize(translated_img, None, fx=scale_factor, fy=scale_factor)

# Mostrar las imágenes
cv.imshow('Imagen Original', img)
cv.imshow('Imagen Rotada y Trasladada', scaled_img)
cv.waitKey(0)
cv.destroyAllWindows()