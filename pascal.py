import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

window_width = 800
window_height = 600
rows = 10  # Número de filas del triángulo de Pascal

def initialize_opengl():
    """Configura OpenGL para la perspectiva y las propiedades iniciales."""
    glClearColor(0, 0, 0, 1)  # Fondo negro
    glEnable(GL_DEPTH_TEST)   # Habilitar la prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, window_width / window_height, 1, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -11)  # Retroceder la cámara


def main():
    """Función principal."""
    # Inicializar GLFW
    if not glfw.init():
        return

    # Crear ventana
    window = glfw.create_window(window_width, window_height, "Triángulo de Pascal", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Configurar OpenGL
    initialize_opengl()

    # Bucle principal de renderizado
    while not glfw.window_should_close(window):
        glfw.poll_events()  # Gestionar eventos (como el cierre de la ventana)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar buffer
        draw_triangle(rows)  # Dibujar el triángulo de Pascal
        glfw.swap_buffers(window)  # Mostrar la imagen renderizada

    glfw.terminate()  # Terminar GLFW

if __name__ == "__main__":
    main()
