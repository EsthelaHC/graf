import numpy as np 
import cv2

# Función para generar un punto en varias formas
def generar_punto(param, equation, t):
    if equation == 'elipse':
        x = int(param[0] * np.cos(t) + 300) 
        y = int(param[1] * np.sin(t) + 300)
    elif equation == 'circunferencia':
        r = param[0]
        x = int(r * np.cos(t) + 300)
        y = int(r * np.sin(t) + 300)
    elif equation == 'parabola':
        x = int(t + 300)
        y = int(param[0] * (t ** 2) + 300)
    elif equation == 'hiperbola':
        x = int(param[0] * np.cosh(t) + 300)
        y = int(param[1] * np.sinh(t) + 300)
    elif equation == 'linea':
        x = int(param[0] * t + param[1] + 300)  # m * t + b
        y = int(param[2] * t + param[3] + 300)  # n * t + k
    elif equation == 'espiral':
        x = int(param[0] * t * np.cos(t) + 300)
        y = int(param[0] * t * np.sin(t) + 300)
    elif equation == 'elipse_desplazada':
        x = int(param[0] * np.cos(t) + 300) 
        y = int(param[1] * np.sin(t) + 150)  # Desplazado verticalmente
    elif equation == 'lemniscata':
        x = int(param[0] * np.cos(t) / (1 + np.sin(t)**2) + 300)
        y = int(param[0] * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2) + 300)
    elif equation == 'cardioide':
        x = int(param[0] * (1 - np.cos(t)) * np.cos(t) + 300)
        y = int(param[0] * (1 - np.cos(t)) * np.sin(t) + 300)
    elif equation == 'cicloide':
        x = int(param[0] * (t - np.sin(t)) + 300)
        y = int(param[0] * (1 - np.cos(t)) + 300)
    return (x, y)

# Inicializar dimensiones de la imagen
img_width, img_height = 600, 600

# Parámetros para las distintas ecuaciones
parametros = {
    'elipse': (200, 100),
    'circunferencia': (100,),
    'parabola': (0.01,),  # a = 0.01
    'hiperbola': (100, 50),  # a, b
    'linea': (1, 0, 1, 100),  # m, b, n, k
    'espiral': (0.1,),
    'elipse_desplazada': (200, 100),
    'lemniscata': (100,),
    'cardioide': (100,),
    'cicloide': (50,)
}

# Número de puntos a generar
num_puntos = 1000
t_vals = np.linspace(0, 2 * np.pi, num_puntos)

# Dibujar las formas en diferentes ventanas
for equation, param in parametros.items():
    imagen = np.zeros((img_height, img_width, 3), dtype=np.uint8)  # Crear una nueva imagen para cada ecuación

    for t in t_vals:
        punto = generar_punto(param, equation, t)
        cv2.circle(imagen, punto, radius=5, color=(0, 255, 0), thickness=-1)

        # También dibujar puntos de la trayectoria
        for t_tray in t_vals:
            pt_tray = generar_punto(param, equation, t_tray)
            cv2.circle(imagen, pt_tray, radius=1, color=(255, 255, 255), thickness=-1)

    # Mostrar cada ecuación en su propia ventana
    cv2.imshow(f'Figura: {equation}', imagen)
    cv2.waitKey(0)  # Esperar a que se presione una tecla para continuar a la siguiente figura

cv2.destroyAllWindows()
