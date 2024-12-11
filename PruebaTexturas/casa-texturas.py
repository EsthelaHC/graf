import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PIL import Image
import sys

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad
    glEnable(GL_TEXTURE_2D)           # Activar texturas

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 6.0, 100.0)  # Campo de visión
    glMatrixMode(GL_MODELVIEW)

def load_texture(filename):
    """Carga una textura desde un archivo de imagen"""
    img = Image.open(filename)
    img_data = img.tobytes("raw", "RGB", 0, -1)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def draw_textured_quad(vertices, tex_coords, texture_id):
    """Dibuja un cuadrado con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for i in range(4):
        glTexCoord2f(*tex_coords[i])
        glVertex3f(*vertices[i])
    glEnd()

def draw_house(wall_texture, roof_texture, floor_texture, door_texture, window_texture):
    """Dibuja una casa con texturas"""
    # Paredes de la casa
    walls = [
        ([-1.5, 0, 1], [1.5, 0, 1], [1.5, 3, 1], [-1.5, 3, 1]),  # Frente
        ([-1.5, 0, -1], [1.5, 0, -1], [1.5, 3, -1], [-1.5, 3, -1]),  # Atrás
        ([-1.5, 0, -1], [-1.5, 0, 1], [-1.5, 3, 1], [-1.5, 3, -1]),  # Izquierda
        ([1.5, 0, -1], [1.5, 0, 1], [1.5, 3, 1], [1.5, 3, -1])   # Derecha
    ]
    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for wall in walls:
        draw_textured_quad(wall, tex_coords, wall_texture)

    # Techo
    roof = [
        ([-2, 3, 1], [2, 3, 1], [0, 5, 0]),  # Frente
        ([-2, 3, -1], [2, 3, -1], [0, 5, 0]),  # Atrás
        ([-2, 3, -1], [-2, 3, 1], [0, 5, 0]),  # Izquierda
        ([2, 3, -1], [2, 3, 1], [0, 5, 0])   # Derecha
    ]
    glBindTexture(GL_TEXTURE_2D, roof_texture)
    glBegin(GL_TRIANGLES)
    for tri in roof:
        for vertex in tri:
            glTexCoord2f((vertex[0] + 2) / 4, (vertex[2] + 1) / 2)
            glVertex3f(*vertex)
    glEnd()

    # Suelo
    floor = [(-1.5, 0, -1), (1.5, 0, -1), (1.5, 0, 1), (-1.5, 0, 1)]
    draw_textured_quad(floor, tex_coords, floor_texture)

    # Puerta
    door = [(-0.4, 0, 1.01), (0.4, 0, 1.01), (0.4, 1.5, 1.01), (-0.4, 1.5, 1.01)]
    draw_textured_quad(door, tex_coords, door_texture)

    # Ventanas
    windows = [
        [(-0.9, 1.5, 1.01), (-0.4, 1.5, 1.01), (-0.4, 2.5, 1.01), (-0.9, 2.5, 1.01)],  # Izquierda
        [(0.4, 1.5, 1.01), (0.9, 1.5, 1.01), (0.9, 2.5, 1.01), (0.4, 2.5, 1.01)]   # Derecha
    ]
    for window in windows:
        draw_textured_quad(window, tex_coords, window_texture)

def draw_scene(wall_texture, roof_texture, floor_texture, door_texture, window_texture):
    """Dibuja la escena completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(10, 8, 15, 0, 0, 0, 0, 1, 0)

    draw_house(wall_texture, roof_texture, floor_texture, door_texture, window_texture)
    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()

    # Crear ventana
    width, height = 800, 600
    window = glfw.create_window(width, height, "Casa con Texturas", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Cargar texturas
    wall_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\pared.jpg") #paredes
    roof_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\tejado.jpg") #tejado
    floor_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\ground.jpg") #suelo
    door_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\puerta.jpg") #puerta
    window_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\ventanas.jpeg") #ventanas

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene(wall_texture, roof_texture, floor_texture, door_texture, window_texture)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

