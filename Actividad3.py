import cv2 as cv
import numpy as np

# Cargar la imagen
img =cv.imread(r"hongos.jpg",0)

# Dimensiones de la imagen
x, y = img.shape[0], img.shape[1]

# Rotación de 70 grados con escalado de 2
angle = 70
scale_factor = 2
rotation_matrix = cv.getRotationMatrix2D((y // 2, x // 2), angle, scale_factor)
rotated_img = cv.warpAffine(img, rotation_matrix, (y * scale_factor, x * scale_factor))

# Traslación de 20 píxeles en x e y
tx, ty = 20, 20  
translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
translated_img = cv.warpAffine(rotated_img, translation_matrix, (int(y * scale_factor), int(x * scale_factor)))

# Mostrar la imagen transformada
cv.imshow('Imagen Rotada, Escalada y Trasladada', translated_img)

cv.waitKey(0)
cv.destroyAllWindows()