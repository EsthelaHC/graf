import numpy as np
import cv2 as cv
import math

cap = cv.VideoCapture(0)

lkparm = dict(winSize=(15, 15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

_, vframe = cap.read()
vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)

# Definir puntos de control en posiciones específicas de la pantalla
p0 = np.array([(50, 50), (500, 50), (50, 400)])  # Traslación en la esquina superior izquierda, Escalado en la esquina superior derecha, Rotación en la parte inferior izquierda
p0 = np.float32(p0[:, np.newaxis, :])

mask = np.zeros_like(vframe)

# Cargar la imagen PNG con canal alfa
png_image = cv.imread(r"C:\Users\esthe\Desktop\Grafi\PROYECTO-1\Manzana.png", cv.IMREAD_UNCHANGED)

# Parámetros de control
limTrasPos = 100  # Máximo de traslación a la derecha
limTrasNeg = -100  # Máximo de traslación a la izquierda
conTras = 0  # Contador de la traslación

limEscMax = 3.0  # Máximo factor de escalamiento
limEscMin = 0.6  # Mínimo factor de escalamiento
conEsc = 1  # Factor de escalamiento inicial

limRotHoraria = 360
limRotAntiHorario = -360
conRot = 0  # Ángulo de rotación inicial

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    fgris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    p1, st, err = cv.calcOpticalFlowPyrLK(vgris, fgris, p0, None, **lkparm)

    # Dimensiones del marco
    alto, ancho, _ = frame.shape
    tamano = int(100 * conEsc)  # Tamaño de la imagen según el factor de escalado

    # Redimensiona la imagen PNG según el tamaño
    resized_png = cv.resize(png_image, (tamano, tamano))
    
    x, y = resized_png.shape[:2]
    centro_imagen = (y // 2, x // 2)
    Matriz_rotacion = cv.getRotationMatrix2D(centro_imagen, conRot, 1.0)
    
    imagen_rotada = cv.warpAffine(resized_png, Matriz_rotacion, (y,x))

    # Separar los canales de la máscara
    mascara_rgb = imagen_rotada[:, :, :3]
    mascara_alpha = imagen_rotada[:, :, 3]
    
    # Determinar la posición central
    x_centro = (ancho - tamano) // 2 + conTras
    y_centro = (alto - tamano) // 2

    # Crear una región de interés (ROI) en el centro del frame
    roi = frame[y_centro:y_centro + tamano, x_centro:x_centro + tamano]
    
    # Combinar la máscara con el ROI del frame
    mascara_alpha_inv = cv.bitwise_not(mascara_alpha)
    fondo = cv.bitwise_and(roi, roi, mask=mascara_alpha_inv)
    mascara_fg = cv.bitwise_and(mascara_rgb, mascara_rgb, mask=mascara_alpha)
    resultado = cv.add(fondo, mascara_fg)

    # Colocar la imagen combinada en el centro del frame
    frame[y_centro:y_centro + tamano, x_centro:x_centro + tamano] = resultado

    if p1 is None:
        vgris = cv.cvtColor(vframe, cv.COLOR_BGR2GRAY)
        p0 = np.array([(50, 50), (500, 50), (50, 400)])  # Actualizar las posiciones de los puntos
        p0 = np.float32(p0[:, np.newaxis, :])
        mask = np.zeros_like(vframe)
        cv.imshow('ventana', frame)
    else:
        bp1 = p1[st == 1]
        bp0 = p0[st == 1]

        # Variables para mover la imagen con los puntos de control
        T0x, T0y, T1x, T1y, R4x, R4y = 0, 0, 0, 0, 0, 0

        for i, (nv, vj) in enumerate(zip(bp1, bp0)):
            a, b = (int(x) for x in nv.ravel())
            c, d = (int(x) for x in vj.ravel())

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
                T0x = c - a
                T0y = d - b
            if i == 1:  # Puntos de control para escalado
                T1x = c - a
                T1y = d - b
            if i == 2:  # Puntos de control para rotación
                R4x = c - a
                R4y = d - b

        # Traslación (control por el punto 0)
        if abs(T0x) > 10:  # Consideramos el desplazamiento solo si hay un cambio considerable en X
            conTras += T0x // 10  # Aplicar el cambio en X de manera más gradual
            conTras = max(min(conTras, limTrasPos), limTrasNeg)  # Limitar el rango de traslación

        # Escalado (control por el punto 1)
        if abs(T1x) > 10 and abs(T1y) > 5:
            if T1x > 0: 
                conEsc += 0.2  # Aumenta el escalado si el punto se mueve hacia la derecha
            elif T1x < 0:
                conEsc -= 0.2  # Disminuye el escalado si el punto se mueve hacia la izquierda
            conEsc = max(min(conEsc, limEscMax), limEscMin)  # Limita el escalado

        # Rotación (control por el punto 2)
        if abs(R4x) > 10 and abs(R4y) > 5:
            if R4x > 0: 
                conRot += 5  # Aumenta la rotación si el punto se mueve hacia la derecha
            elif R4x < 0:
                conRot -= 5  # Disminuye la rotación si el punto se mueve hacia la izquierda
            conRot = max(min(conRot, limRotHoraria), limRotAntiHorario)  # Limita la rotación

        cv.imshow('ventana', frame)
        vgris = fgris.copy()

    if (cv.waitKey(1) & 0xff) == 27:  # Salir con 'Esc'
        break

cap.release()
cv.destroyAllWindows()
