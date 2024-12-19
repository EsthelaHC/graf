import numpy as np
import cv2 as cv
import math

# Inicialización de la captura de video
video_captura = cv.VideoCapture(0)

# Parámetros para el flujo óptico de Lucas-Kanade
parametros_lk = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# Leer el primer cuadro del video y convertirlo a escala de grises
_, cuadro_inicial = video_captura.read()
cuadro_gris_anterior = cv.cvtColor(cuadro_inicial, cv.COLOR_BGR2GRAY)

# Definir puntos de control en posiciones específicas de la pantalla
puntos_iniciales = np.array([(50, 50), (500, 50), (50, 400)])  # Traslación, Escalado, Rotación
puntos_iniciales = np.float32(puntos_iniciales[:, np.newaxis, :])

# Crear una máscara vacía del mismo tamaño que el cuadro
mascara_dibujo = np.zeros_like(cuadro_inicial)

# Cargar la imagen PNG con canal alfa
imagen_png = cv.imread(r"C:\\Users\\esthe\\Desktop\\Grafi\\PROYECTO-1\\Manzana.png", cv.IMREAD_UNCHANGED)

# Parámetros de transformación
limite_traslacion_derecha = 200
limite_traslacion_izquierda = -200
contador_traslacion = 0

factor_escalado_maximo = 5.0
factor_escalado_minimo = 0.6
factor_escalado_actual = 1

rotacion_maxima_horaria = 360
rotacion_maxima_antihoraria = -360
angulo_rotacion_actual = 0

while True:
    # Capturar el cuadro actual y convertirlo a escala de grises
    _, cuadro_actual = video_captura.read()
    cuadro_actual = cv.flip(cuadro_actual, 1)
    cuadro_gris_actual = cv.cvtColor(cuadro_actual, cv.COLOR_BGR2GRAY)

    # Calcular el flujo óptico
    puntos_siguientes, estado, error = cv.calcOpticalFlowPyrLK(
        cuadro_gris_anterior, cuadro_gris_actual, puntos_iniciales, None, **parametros_lk
    )

    # Dimensiones del cuadro actual
    alto_cuadro, ancho_cuadro, _ = cuadro_actual.shape
    tamano_imagen = int(100 * factor_escalado_actual)

    # Redimensionar la imagen PNG según el factor de escalado
    imagen_redimensionada = cv.resize(imagen_png, (tamano_imagen, tamano_imagen))

    # Rotar la imagen
    alto_imagen, ancho_imagen = imagen_redimensionada.shape[:2]
    centro_imagen = (ancho_imagen // 2, alto_imagen // 2)
    matriz_rotacion = cv.getRotationMatrix2D(centro_imagen, angulo_rotacion_actual, 1.0)
    imagen_rotada = cv.warpAffine(imagen_redimensionada, matriz_rotacion, (ancho_imagen, alto_imagen))

    # Separar canales RGB y alfa
    canal_rgb = imagen_rotada[:, :, :3]
    canal_alfa = imagen_rotada[:, :, 3]

    # Determinar la posición central de la imagen
    posicion_x = (ancho_cuadro - tamano_imagen) // 2 + contador_traslacion
    posicion_y = (alto_cuadro - tamano_imagen) // 2

    # Crear una región de interés (ROI) en el cuadro actual
    region_interes = cuadro_actual[posicion_y:posicion_y + tamano_imagen, posicion_x:posicion_x + tamano_imagen]

    # Combinar la imagen con la región de interés usando la máscara alfa
    canal_alfa_invertido = cv.bitwise_not(canal_alfa)
    fondo = cv.bitwise_and(region_interes, region_interes, mask=canal_alfa_invertido)
    primer_plano = cv.bitwise_and(canal_rgb, canal_rgb, mask=canal_alfa)
    resultado_combinado = cv.add(fondo, primer_plano)

    # Colocar la imagen combinada de nuevo en el cuadro actual
    cuadro_actual[posicion_y:posicion_y + tamano_imagen, posicion_x:posicion_x + tamano_imagen] = resultado_combinado

    if puntos_siguientes is None:
        cuadro_gris_anterior = cv.cvtColor(cuadro_inicial, cv.COLOR_BGR2GRAY)
        puntos_iniciales = np.array([(50, 50), (500, 50), (50, 400)])
        puntos_iniciales = np.float32(puntos_iniciales[:, np.newaxis, :])
        mascara_dibujo = np.zeros_like(cuadro_inicial)
        cv.imshow('Ventana', cuadro_actual)
    else:
        puntos_buenos_actuales = puntos_siguientes[estado == 1]
        puntos_buenos_iniciales = puntos_iniciales[estado == 1]

        # Variables de control de movimiento
        movimiento_traslacion_x, movimiento_traslacion_y = 0, 0
        movimiento_escalado_x, movimiento_escalado_y = 0, 0
        movimiento_rotacion_x, movimiento_rotacion_y = 0, 0

        for i, (punto_actual, punto_inicial) in enumerate(zip(puntos_buenos_actuales, puntos_buenos_iniciales)):
            x_actual, y_actual = (int(coord) for coord in punto_actual.ravel())
            x_inicial, y_inicial = (int(coord) for coord in punto_inicial.ravel())

            # Dibujar los puntos y sus etiquetas
            cuadro_actual = cv.line(cuadro_actual, (x_inicial, y_inicial), (x_actual, y_actual), (0, 0, 255), 2)
            cuadro_actual = cv.circle(cuadro_actual, (x_inicial, y_inicial), 2, (255, 0, 0), -1)
            cuadro_actual = cv.circle(cuadro_actual, (x_actual, y_actual), 3, (0, 255, 0), -1)

            if i == 0:  # Traslación
                cv.putText(cuadro_actual, 'Traslacion', (x_actual + 10, y_actual - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv.LINE_AA)
                movimiento_traslacion_x = x_inicial - x_actual
            elif i == 1:  # Escalado
                cv.putText(cuadro_actual, 'Escalado', (x_actual + 10, y_actual - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)
                movimiento_escalado_x = x_inicial - x_actual
            elif i == 2:  # Rotación
                cv.putText(cuadro_actual, 'Rotacion', (x_actual + 10, y_actual - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)
                movimiento_rotacion_x = x_inicial - x_actual

        # Actualizar traslación
        if abs(movimiento_traslacion_x) > 10:
            contador_traslacion += movimiento_traslacion_x // 10
            contador_traslacion = max(
                min(contador_traslacion, limite_traslacion_derecha), limite_traslacion_izquierda
            )

        # Actualizar escalado
        if abs(movimiento_escalado_x) > 10:
            if movimiento_escalado_x > 0:
                factor_escalado_actual += 0.2
            else:
                factor_escalado_actual -= 0.2
            factor_escalado_actual = max(
                min(factor_escalado_actual, factor_escalado_maximo), factor_escalado_minimo
            )

        # Actualizar rotación
        if abs(movimiento_rotacion_x) > 10:
            if movimiento_rotacion_x > 0:
                angulo_rotacion_actual += 5
            else:
                angulo_rotacion_actual -= 5
            angulo_rotacion_actual = max(
                min(angulo_rotacion_actual, rotacion_maxima_horaria), rotacion_maxima_antihoraria
            )

        cv.imshow('Ventana', cuadro_actual)
        cuadro_gris_anterior = cuadro_gris_actual.copy()

    if (cv.waitKey(1) & 0xFF) == 27:  # Salir con 'Esc'
        break

video_captura.release()
cv.destroyAllWindows()
