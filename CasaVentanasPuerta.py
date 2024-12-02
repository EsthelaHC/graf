import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, 6, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.6, 0.4, 0.5)  # lila para todas las caras

    # Frente
    glVertex3f(-1.5, 0, 1)
    glVertex3f(1.5, 0, 1)
    glVertex3f(1.5, 3, 1)
    glVertex3f(-1.5, 3, 1)

    # Atrás     X  Y   Z
    glVertex3f(-1.5, 0, -1)
    glVertex3f(1.5, 0, -1)
    glVertex3f(1.5, 3, -1)
    glVertex3f(-1.5, 3, -1)

    # Izquierda
    glVertex3f(-1.5, 0, -1)
    glVertex3f(-1.5, 0, 1)
    glVertex3f(-1.5, 3, 1)
    glVertex3f(-1.5, 3, -1)

    # Derecha
    glVertex3f(1.5, 0, -1)
    glVertex3f(1.5, 0, 1)
    glVertex3f(1.5, 3, 1)
    glVertex3f(1.5, 3, -1)

    # Arriba
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para el techo
    glVertex3f(-1.5, 3, -1)
    glVertex3f(1.5, 3, -1)
    glVertex3f(1.5, 3, 1)
    glVertex3f(-1.5, 3, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glVertex3f(-1.5,0 , -1)
    glVertex3f(1.5, 0, -1)
    glVertex3f(1.5, 0, 1)
    glVertex3f(-1.5, 0, 1)
    glEnd()

def draw_roof():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.6, 0.1, 0.1)  # Rojo bajo

    # Frente
    glVertex3f(-2, 3, 1)
    glVertex3f(2, 3, 1)
    glVertex3f(0, 5, 0)  #Reduce la altura del vértice superior

    # Atrás
    glVertex3f(-2, 3, -1)
    glVertex3f(2, 3, -1)
    glVertex3f(0, 5, 0)  #Reduce la altura del vértice superior

    # Izquierda
    glVertex3f(-2, 3, -1)
    glVertex3f(-2, 3, 1)
    glVertex3f(0, 5, 0)  #Reduce la altura del vértice superior

    # Derecha
    glVertex3f(2, 3, -1)
    glVertex3f(2, 3, 1)
    glVertex3f(0, 5, 0)  #Reduce la altura del vértice superior

    glEnd()

def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()
    
def draw_door():
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.2, 0.1)  # Marrón oscuro para la puerta
    glVertex3f(-0.4, 0, 1.01)
    glVertex3f(0.4, 0, 1.01)
    glVertex3f(0.4, 1.5, 1.01)
    glVertex3f(-0.4, 1.5, 1.01)
    glEnd()

def draw_rectangular_windows():
    """Dibuja ventanas rectangulares con marcos y divisiones."""
    glColor3f(0.6, 0.8, 1.0)  # Azul claro para el vidrio

    # Ventana izquierda
    glBegin(GL_QUADS)
    glVertex3f(-0.9, 1.5, 1.01)  # Punto superior izquierdo 
    glVertex3f(-0.4, 1.5, 1.01)  # Punto superior derecho 
    glVertex3f(-0.4, 2.5, 1.01)  # Punto inferior derecho 
    glVertex3f(-0.9, 2.5, 1.01)  # Punto inferior izquierdo 
    glEnd()

    # Ventana derecha
    glBegin(GL_QUADS)
    glVertex3f(0.4, 1.5, 1.01)   # Punto superior izquierdo
    glVertex3f(0.9, 1.5, 1.01)   # Punto superior derecho
    glVertex3f(0.9, 2.5, 1.01)   # Punto inferior derecho 
    glVertex3f(0.4, 2.5, 1.01)   # Punto inferior izquierdo
    glEnd()

    # Marco de las ventanas
    glColor3f(0.0, 0.0, 0.0)  # Negro para el marco
    glLineWidth(2)  # Ajustar grosor del marco
    glBegin(GL_LINE_LOOP)  # Marco ventana izquierda
    glVertex3f(-0.9, 1.5, 1.01)  # Punto superior izquierdo
    glVertex3f(-0.4, 1.5, 1.01)  # Punto superior derecho 
    glVertex3f(-0.4, 2.5, 1.01)  # Punto inferior derecho 
    glVertex3f(-0.9, 2.5, 1.01)  # Punto inferior izquierdo
    glEnd()

    glBegin(GL_LINE_LOOP)  # Marco ventana derecha
    glVertex3f(0.4, 1.5, 1.01)   # Punto superior izquierdo
    glVertex3f(0.9, 1.5, 1.01)   # Punto superior derecho
    glVertex3f(0.9, 2.5, 1.01)   # Punto inferior derecho 
    glVertex3f(0.4, 2.5, 1.01)   # Punto inferior izquierdo 
    glEnd()

    # Divisiones internas de las ventanas
    glBegin(GL_LINES)
    glVertex3f(-0.65, 1.5, 1.01)  # División vertical izquierda 
    glVertex3f(-0.65, 2.5, 1.01)  # División vertical izquierda

    glVertex3f(0.65, 1.5, 1.01)  # División vertical derecha
    glVertex3f(0.65, 2.5, 1.01)  # División vertical derecha

    glVertex3f(-0.9, 2, 1.01)  # División horizontal izquierda 
    glVertex3f(-0.4, 2, 1.01)  # División horizontal izquierda 

    glVertex3f(0.4, 2, 1.01)  # División horizontal derecha 
    glVertex3f(0.9, 2, 1.01)  # División horizontal derecha 
    glEnd()

    # Reflejos simples en las ventanas
    glColor3f(1.0, 1.0, 1.0)  # Blanco para los reflejos
    glBegin(GL_LINES)
    glVertex3f(-0.9, 2.5, 1.01)  # Reflejo diagonal izquierda 
    glVertex3f(-0.65, 2, 1.01)

    glVertex3f(0.4, 2.5, 1.01)  # Reflejo diagonal derecha 
    glVertex3f(0.65, 2, 1.01)
    glEnd()

    
def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()  # Base de la casa
    draw_roof()  # Techo
    draw_door()  # Puerta
    draw_rectangular_windows() #ventanas fijas

def draw_scene():
    """Dibuja toda la escena con 4 casas"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(10, 8, 15,  # Posición de la cámara
              0, 0, 0,    # Punto al que mira
              0, 1, 0)    # Vector hacia arriba

    # Dibujar el suelo
    draw_ground()

    # Dibujar las casas en diferentes posiciones
    positions = [
        (-5, 0, -5),  # casa 1
        (5, 0, -5),   # casa 2
        (-5, 0, 5),   # casa 3
        (5, 0, 5),    # casa 4
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual
        draw_house()        # Dibujar la casa
        glPopMatrix()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Casa con ventanas y puerta", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
