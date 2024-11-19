import cv2 as cv
import numpy as np

# Cargar la imagen
img =cv.imread(r"hongos.jpg",0)

# Dimensiones de la imagen
x, y = img.shape[0], img.shape[1]

# Rotación de 30 grados hacia la derecha
angle_right = 30
rotation_matrix_right = cv.getRotationMatrix2D((y // 2, x // 2), angle_right, 2)  # Escalar con factor 2
rotated_right_img = cv.warpAffine(img, rotation_matrix_right, (y * 2, x * 2))

# Rotación de 60 grados hacia la izquierda
angle_left = -60
rotation_matrix_left = cv.getRotationMatrix2D((y // 2, x // 2), angle_left, 2)  # Escalar con factor 2
rotated_left_img = cv.warpAffine(img, rotation_matrix_left, (y * 2, x * 2))

# Mostrar las imágenes
cv.imshow('Imagen Original', img)
cv.imshow('Rotada 30 grados a la derecha y escalada', rotated_right_img)
cv.imshow('Rotada 60 grados a la izquierda y escalada', rotated_left_img)
cv.waitKey(0)
cv.destroyAllWindows()