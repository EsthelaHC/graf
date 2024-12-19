import numpy as np
import cv2 as cv
import math

cap = cv.VideoCapture(0)

lk_parametros = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, frame_inicial = cap.read()
frame_gris = cv.cvtColor(frame_inicial, cv.COLOR_BGR2GRAY)

# Definir puntos de control en posiciones específicas de la pantalla
puntos_control_iniciales = np.array([(50, 50), (500, 50), (50, 400)])  # Traslación, Escalado, Rotación
puntos_control_iniciales = np.float32(puntos_control_iniciales[:, np.newaxis, :])

mascara = np.zeros_like(frame_inicial)

# Cargar la imagen PNG con canal alfa
imagen_manzana = cv.imread(r"C:\Users\esthe\Desktop\Grafi\PROYECTO-1\Manzana.png", cv.IMREAD_UNCHANGED)

# Parámetros de control
limite_traslacion_pos = 100  # Máximo de traslación a la derecha
limite_traslacion_neg = -100  # Máximo de traslación a la izquierda
traslacion = 0  # Contador de la traslación

limite_escalado_max = 3.0  # Máximo factor de escalamiento
limite_escalado_min = 0.6  # Mínimo factor de escalamiento
factor_escalado = 1  # Factor de escalado inicial

limite_rotacion_horaria = 360
limite_rotacion_antihoraria = -360
angulo_rotacion = 0  # Ángulo de rotación inicial

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame_gris_actualizado = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    puntos_control_actualizados, estado_puntos, error_seguimiento = cv.calcOpticalFlowPyrLK(frame_gris, frame_gris_actualizado, puntos_control_iniciales, None, **lk_parametros)

    # Dimensiones del marco
    alto, ancho, _ = frame.shape
    tamano_imagen = int(100 * factor_escalado)  # Tamaño de la imagen según el factor de escalado

    # Redimensiona la imagen PNG según el tamaño
    imagen_manzana_redimensionada = cv.resize(imagen_manzana, (tamano_imagen, tamano_imagen))
    
    x, y = imagen_manzana_redimensionada.shape[:2]
    centro_imagen = (y // 2, x // 2)
    matriz_rotacion = cv.getRotationMatrix2D(centro_imagen, angulo_rotacion, 1.0)
    
    imagen_rotada = cv.warpAffine(imagen_manzana_redimensionada, matriz_rotacion, (y, x))

    # Separar los canales de la máscara
    mascara_rgb = imagen_rotada[:, :, :3]
    mascara_alpha = imagen_rotada[:, :, 3]
    
    # Determinar la posición central
    x_centro = (ancho - tamano_imagen) // 2 + traslacion
    y_centro = (alto - tamano_imagen) // 2

    # Crear una región de interés (ROI) en el centro del frame
    roi = frame[y_centro:y_centro + tamano_imagen, x_centro:x_centro + tamano_imagen]
    
    # Combinar la máscara con el ROI del frame
    mascara_alpha_inversa = cv.bitwise_not(mascara_alpha)
    fondo = cv.bitwise_and(roi, roi, mask=mascara_alpha_inversa)
    mascara_fg = cv.bitwise_and(mascara_rgb, mascara_rgb, mask=mascara_alpha)
    resultado = cv.add(fondo, mascara_fg)

    # Colocar la imagen combinada en el centro del frame
    frame[y_centro:y_centro + tamano_imagen, x_centro:x_centro + tamano_imagen] = resultado

    if puntos_control_actualizados is None:
        frame_gris = cv.cvtColor(frame_inicial, cv.COLOR_BGR2GRAY)
        puntos_control_iniciales = np.array([(50, 50), (500, 50), (50, 400)])  # Actualizar las posiciones de los puntos
        puntos_control_iniciales = np.float32(puntos_control_iniciales[:, np.newaxis, :])
        mascara = np.zeros_like(frame_inicial)
        cv.imshow('ventana', frame)
    else:
        puntos_control_validos = puntos_control_actualizados[estado_puntos == 1]
        puntos_control_iniciales_validos = puntos_control_iniciales[estado_puntos == 1]

        # Variables para mover la imagen con los puntos de control
        traslacion_x, traslacion_y, escalado_x, escalado_y, rotacion_x, rotacion_y = 0, 0, 0, 0, 0, 0

        for i, (nuevo_punto, punto_original) in enumerate(zip(puntos_control_validos, puntos_control_iniciales_validos)):
            a, b = (int(x) for x in nuevo_punto.ravel())
            c, d = (int(x) for x in punto_original.ravel())

            # Dibuja las líneas de los puntos
            frame = cv.line(frame, (c, d), (a, b), (0, 0, 255), 2)  
            frame = cv.circle(frame, (c, d), 2, (255, 0, 0), -1)  # Dibuja los puntos originales
            frame = cv.circle(frame, (a, b), 3, (0, 255, 0), -1)  # Dibuja los puntos actualizados

            # Etiquetas para indicar cuál es cada punto
            if i == 0:  # Traslación
                cv.putText(frame, 'Traslacion', (a + 10, b - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv.LINE_AA)
            elif i == 1:  # Escalado
                cv.putText(frame, 'Escalado', (a + 10, b - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv.LINE_AA)
            elif i == 2:  # Rotación
                cv.putText(frame, 'Rotacion', (a + 10, b - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv.LINE_AA)

            # Calculamos el desplazamiento
            distancia = math.sqrt((c - a) ** 2 + (d - b) ** 2)
            if i == 0:  # Puntos de control para traslación
                traslacion_x = c - a
                traslacion_y = d - b
            if i == 1:  # Puntos de control para escalado
                escalado_x = c - a
                escalado_y = d - b
            if i == 2:  # Puntos de control para rotación
                rotacion_x = c - a
                rotacion_y = d - b

        # Traslación (control por el punto 0)
        if abs(traslacion_x) > 10:  # Consideramos el desplazamiento solo si hay un cambio considerable en X
            traslacion += traslacion_x // 10  # Aplicar el cambio en X de manera más gradual
            traslacion = max(min(traslacion, limite_traslacion_pos), limite_traslacion_neg)  # Limitar el rango de traslación

        # Escalado (control por el punto 1)
        if abs(escalado_x) > 10 and abs(escalado_y) > 5:
            if escalado_x > 0: 
                factor_escalado += 0.1
            else:
                factor_escalado -= 0.1
            factor_escalado = max(min(factor_escalado, limite_escalado_max), limite_escalado_min)

        # Rotación (control por el punto 2)
        if abs(rotacion_x) > 10 and abs(rotacion_y) > 10:
            angulo_rotacion += (rotacion_x + rotacion_y) // 2  # Tomamos un promedio de los desplazamientos
            angulo_rotacion = max(min(angulo_rotacion, limite_rotacion_horaria), limite_rotacion_antihoraria)

    cv.imshow('ventana', frame)

    if (cv.waitKey(1) & 0xff) == 27:  # Si el usuario presiona 'Esc', se cierra el bucle
        break

cap.release()
cv.destroyAllWindows()
