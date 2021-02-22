from OpenGL.GL import *
from glew_wish import *
import glfw
from math import *
import random
from enum import Enum

xJugador1 = -0.9
yJugador1 = 0.0
puntosJugador1 = 0

xJugador2 = 0.9
yJugador2 = 0.0
puntosJugador2 = 0

colisionando = False

xPelota = 0.0
yPelota = 0.0
angulo = random.randrange(30, 180)

# El desfase es debido a que en 0 grados se voltea hacia arriba y no hacia la derecha
desfase = 90
velocidad = 1
tiempo_anterior = 0

def actualizar_pelota(tiempo_delta):
    global xPelota
    global yPelota
    global velocidad

    yPelota = yPelota + (sin((angulo + desfase) * 3.14159 / 180) * 0.75 * tiempo_delta)
    xPelota = xPelota + (cos((angulo + desfase) * 3.14159 / 180) * 0.75 * tiempo_delta)

def checar_colisiones():
    global colisionando
    global xPelota
    global yPelota
    global angulo
    
    # Checar colision jugadores
    if  xPelota - 0.025 < xJugador1 + 0.025 and xPelota + 0.025 > xJugador1 - 0.0125 and yPelota - 0.1 < yJugador1 + 0.025 and yPelota + 0.1 > yJugador1 - 0.0125:
        angulo -= 90
    elif xPelota - 0.025 < xJugador2 + 0.025 and xPelota + 0.025 > xJugador2 - 0.0125 and yPelota - 0.1 < yJugador2 + 0.025 and yPelota + 0.1 > yJugador2 - 0.0125:
        angulo -= 90
    if xPelota - 0.025 <= -0.975 or xPelota + 0.025 >= 0.975:
        angulo -= 90

    if yPelota - 0.025 <= -0.975 or yPelota + 0.025 >= 0.975:
        angulo -= 90

def actualizar(window):
    global tiempo_anterior
    global xJugador1
    global yJugador1
    global xJugador2
    global yJugador2

    tiempo_actual = glfw.get_time()
    tiempo_delta = tiempo_actual - tiempo_anterior

    # Player 1
    estadoArriba = glfw.get_key(window, glfw.KEY_UP)
    estadoAbajo = glfw.get_key(window, glfw.KEY_DOWN)

    # Player 2
    estadoArriba2 = glfw.get_key(window, glfw.KEY_W)
    estadoAbajo2 = glfw.get_key(window, glfw.KEY_S)

    if estadoArriba == glfw.PRESS:
        if yJugador1 < 0.8:
            yJugador1 = yJugador1 + (sin((0 + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)

    if estadoAbajo == glfw.PRESS:
        if yJugador1 > -0.8:
            yJugador1 = yJugador1 + (sin((180 + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)

    if estadoArriba2 == glfw.PRESS:
        if yJugador2 < 0.8:
            yJugador2 = yJugador2 + (sin((0 + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)

    if estadoAbajo2 == glfw.PRESS:
        if yJugador2 > -0.8:
            yJugador2 = yJugador2 + (sin((180 + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)

    checar_colisiones()
    actualizar_pelota(tiempo_delta)
    tiempo_anterior = tiempo_actual

def dibujarJugador1():
    global colisionando
    global xJugador1
    global yJugador1
    glPushMatrix()
    glTranslate(xJugador1, yJugador1, 0.0)
    glBegin(GL_QUADS)
    if colisionando == True:
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0.025, 0.2, 0.0)
    glVertex3f(0.025, -0.2, 0.0)
    glVertex3f(-0.025, -0.2, 0.0)
    glVertex3f(-0.025, 0.2, 0.0)
    glEnd()
    glPopMatrix()

def dibujarJugador2():
    global colisionando
    global xJugador2
    global yJugador2
    glPushMatrix()
    glTranslate(xJugador2, yJugador2, 0.0)
    glBegin(GL_QUADS)
    if colisionando == True:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(0.0, 0.0, 0.0)
    glVertex3f(0.025, 0.2, 0.0)
    glVertex3f(0.025, -0.2, 0.0)
    glVertex3f(-0.025, -0.2, 0.0)
    glVertex3f(-0.025, 0.2, 0.0)
    glEnd()
    glPopMatrix()

def dibujarPelota():
    global xPelota
    global yPelota
    glPushMatrix()
    glTranslate(xPelota, yPelota, 0.0)
    glBegin(GL_QUADS)
    if colisionando == True:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0.05, 0.05, 0.0)
    glVertex3f(0.05, -0.05, 0.0)
    glVertex3f(-0.05, -0.05, 0.0)
    glVertex3f(-0.05, 0.05, 0.0)
    glEnd()
    glPopMatrix()

def dibujar():
    # Rutinas de dibujo
    dibujarJugador1()
    dibujarJugador2()
    dibujarPelota()

def key_callback(window, key, scancode, action, mods):
    global angulo
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.destroy_window(window)
        glfw.terminate()

def main():
    # Inicia glfw
    if not glfw.init():
        return

    # Crea la ventana, independientemente del SO que usemos
    window = glfw.create_window(800, 800, "Mi ventana", None, None)

    # Configuramos OpenGL
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # Validamos que se cree la ventana
    if not window:
        glfw.terminate()
        return
    # Establecemos el contexto
    glfw.make_context_current(window)

    # Activamos la validación de funciones modernas de OpenGL
    glewExperimental = True

    # Inicializar GLEW
    if glewInit() != GLEW_OK:
        print("No se pudo inicializar GLEW")
        return

    # Obtenemos versiones de OpenGL y Shaders
    version = glGetString(GL_VERSION)
    print(version)

    version_shaders = glGetString(GL_SHADING_LANGUAGE_VERSION)
    print(version_shaders)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        # Establece regiond e dibujo
        glViewport(0, 0, 800, 800)
        # Establece color de borrado
        glClearColor(0.0, 0.5, 1.0, 1)
        # Borra el contenido de la ventana
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar
        actualizar(window)
        dibujar()

        # Preguntar si hubo entradas de perifericos (Teclado, mouse, game pad, etc.)
        glfw.poll_events()
        # Intercambia los buffers
        glfw.swap_buffers(window)

    # Se destruye la ventana para liberar memoria
    glfw.destroy_window(window)
    # Termina los procesos que inició glfw.init
    glfw.terminate()

if __name__ == "__main__":
    main()
