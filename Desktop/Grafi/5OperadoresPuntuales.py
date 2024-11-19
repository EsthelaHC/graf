import cv2 as cv
import numpy as np

# Leer la imagen en escala de grises
img_original = cv.imread('hongos.jpg',0)
cv.imshow('Imagen Original', img_original)

x, y = img_original.shape

# 1. Operador puntual de Umbralizacion 
img_binaria = img_original.copy()
for i in range(x):
    for j in range(y):
        if img_binaria[i, j] > 150:
            img_binaria[i, j] = 255
        else:
            img_binaria[i, j] = 0
cv.imshow('Umbralizacion', img_binaria)

# 2. Operador puntual de Negativo
img_negativo = img_original.copy()
for i in range(x):
    for j in range(y):
        img_negativo[i, j] = 255 - img_negativo[i, j]
cv.imshow('Negativo', img_negativo)

# 3. Operador puntual de escala de grises modificada
img_escalada = img_original.copy()
factor = 1.5
for i in range(x):
    for j in range(y):
        nuevo_valor = img_escalada[i, j] * factor
        img_escalada[i, j] = min(255, int(nuevo_valor))
cv.imshow('Escala de grises', img_escalada)

# 4. Operador puntual de Umbralización inversa
img_inversa = img_original.copy()
for i in range(x):
    for j in range(y):
        if img_inversa[i, j] > 150:
            img_inversa[i, j] = 0
        else:
            img_inversa[i, j] = 255
cv.imshow('umbralizacion inversa', img_inversa)

# 5. Operador puntual de escalado lineal
img_contraste = img_original.copy()
alpha = 1.2  # escala para ajustar el contraste
beta = 30    # Desplazamiento para ajustar el brillo

for i in range(x):
    for j in range(y):
        nuevo_valor = alpha * img_contraste[i, j] + beta
        img_contraste[i, j] = min(255, max(0, int(nuevo_valor)))
cv.imshow('Escalado lineal', img_contraste)

cv.waitKey(0)
cv.destroyAllWindows()
