import cv2
import numpy as np

# Crear una imagen en blanco (una matriz de ceros de 500x500 píxeles con 3 canales para el color)
img = np.zeros((500, 500, 3), dtype=np.uint8)

# Dibujar la base de la casa (un rectángulo)
cv2.rectangle(img, (150, 250), (350, 450), (0, 255, 255), -1)  # Amarillo relleno

# Dibujar el techo de la casa (un triángulo usando polilínea)
pts = np.array([[150, 250], [250, 150], [350, 250]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(img, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
cv2.fillPoly(img, [pts], color=(0, 0, 255))  # Techo relleno rojo

# Dibujar la puerta (otro rectángulo)
cv2.rectangle(img, (225, 350), (275, 450), (139, 69, 19), -1)  # Marrón relleno

# Dibujar ventanas (cuadrados)
cv2.rectangle(img, (175, 275), (225, 325), (255, 255, 255), -1)  # Ventana izquierda
#cv2.rectangle(img, (275, 275), (325, 325), (255, 255, 255), -1)  # Ventana derecha

# Dibujar el sol (un círculo en la esquina superior derecha)
cv2.circle(img, (400, 100), 50, (0, 255, 255), -1)  # Sol amarillo

# Dibujar flores - círculo central y pétalos
def dibujar_flor(img, centro, color_petalos, color_centro):
    # Pétalos (círculos alrededor del centro)
    cv2.circle(img, (centro[0], centro[1] - 15), 10, color_petalos, -1)  # Superior
    cv2.circle(img, (centro[0], centro[1] + 15), 10, color_petalos, -1)  # Inferior
    cv2.circle(img, (centro[0] - 15, centro[1]), 10, color_petalos, -1)  # Izquierda
    cv2.circle(img, (centro[0] + 15, centro[1]), 10, color_petalos, -1)  # Derecha
    # Centro de la flor
    cv2.circle(img, centro, 10, color_centro, -1)

# Dibujar flores de color rosa y azul
# Flor 1 (rosa)
dibujar_flor(img, (100, 460), (255, 192, 203), (255, 255, 0))  # Flor rosa con centro amarillo
# Flor 2 (azul)
dibujar_flor(img, (150, 460), (255, 0, 0), (255, 255, 0))      # Flor azul con centro amarillo
# Flor 3 (rosa)
dibujar_flor(img, (200, 460), (255, 192, 203), (255, 255, 0))  # Flor rosa
# Flor 4 (azul)
dibujar_flor(img, (250, 460), (255, 0, 0), (255, 255, 0))      # Flor azul
# Flor 5 (rosa)
dibujar_flor(img, (300, 460), (255, 192, 203), (255, 255, 0))  # Flor rosa


cv2.imshow('Casa con flores', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
