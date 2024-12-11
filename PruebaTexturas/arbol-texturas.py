import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt, gluNewQuadric, gluCylinder, gluSphere, gluQuadricTexture
from PIL import Image
import sys

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad
    glEnable(GL_LIGHTING)             # Activar luces
    glEnable(GL_LIGHT0)               # Luz básica
    glEnable(GL_COLOR_MATERIAL)       # Materiales de color para reflejar luz
    glShadeModel(GL_SMOOTH)           # Sombreado suave
    glEnable(GL_TEXTURE_2D)           # Activar texturas

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)

    # Luz ambiental y difusa
    light_pos = [10, 10, 10, 1.0]  # Posición de la luz
    light_ambient = [0.3, 0.3, 0.3, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)

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

def draw_trunk(texture_id):
    """Dibuja el tronco del árbol como un cilindro con textura"""
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glColor3f(1.0, 1.0, 1.0)  # Color blanco para mostrar la textura
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(-90, 1, 0, 0)  # Orienta el cilindro verticalmente
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)
    glPopMatrix()

def draw_foliage(texture_id):
    """Dibuja las hojas del árbol como una esfera con textura"""
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glColor3f(1.0, 1.0, 1.0)  # Color blanco para mostrar la textura
    glTranslatef(0.0, 2.0, 0.0)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 1.0, 32, 32)
    glPopMatrix()

def draw_ground(texture_id):
    """Dibuja un plano para representar el suelo con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Color blanco para mostrar la textura
    glTexCoord2f(0.0, 0.0); glVertex3f(-10, 0, 10)
    glTexCoord2f(1.0, 0.0); glVertex3f(10, 0, 10)
    glTexCoord2f(1.0, 1.0); glVertex3f(10, 0, -10)
    glTexCoord2f(0.0, 1.0); glVertex3f(-10, 0, -10)
    glEnd()

def draw_tree(trunk_texture, foliage_texture, ground_texture):
    """Dibuja un árbol completo"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(4, 3, 8,  # Posición de la cámara
              0, 1, 0,  # Punto al que mira
              0, 1, 0)  # Vector hacia arriba

    draw_ground(ground_texture)  # Dibuja el suelo
    draw_trunk(trunk_texture)   # Dibuja el tronco
    draw_foliage(foliage_texture) # Dibuja las hojas

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Árbol 3D con Texturas y Luz", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Carga de texturas
    trunk_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\trunk.jpg")      # Textura para el tronco
    foliage_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\fruta.jpeg") # Textura para las hojas
    ground_texture = load_texture(r"C:\Users\esthe\Desktop\Grafi\PruebaTexturas\ground.jpg")   # Textura para el suelo

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_tree(trunk_texture, foliage_texture, ground_texture)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":

    main()