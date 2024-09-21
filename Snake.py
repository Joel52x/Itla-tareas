import pygame
import time
import random

# Inicializa pygame
pygame.init()
pygame.joystick.init()  # Inicializa el módulo del joystick

# Definir colores
blanco = (255, 255, 255)
verde = (0, 255, 0)
rojo = (213, 50, 80)
negro = (0, 0, 0)
azul = (50, 153, 213)

# Tamaño de la pantalla
ancho = 600
alto = 400
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Snake Game')

# Tamaño del bloque y velocidad de la serpiente
tam_bloque = 20
velocidad = 13

# Fuente para mostrar puntuación
fuente = pygame.font.SysFont(None, 35)

# Función para guardar puntaje en un archivo con nombre
def guardar_puntaje(nombre, puntos):
    with open("puntajes.txt", "a") as archivo:
        archivo.write(f"{nombre}: {puntos}\n")

# Función para mostrar puntajes
def mostrar_mejores_puntajes():
    try:
        with open("puntajes.txt", "r") as archivo:
            puntajes = archivo.readlines()
            puntajes = [linea.strip() for linea in puntajes if linea.strip()]  # Elimina líneas vacías
            puntajes = [linea.split(": ") for linea in puntajes]
            puntajes = [(nombre, int(puntaje)) for nombre, puntaje in puntajes if len(puntaje) > 0]
            puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)[:10]
    except FileNotFoundError:
        puntajes_ordenados = []
    except Exception as e:
        print(f"Error al leer o procesar el archivo: {e}")
        puntajes_ordenados = []

    pantalla.fill(azul)
    y_offset = 50
    if puntajes_ordenados:
        for i, (nombre, puntaje) in enumerate(puntajes_ordenados, start=1):
            texto = fuente.render(f"{i}. {nombre}: {puntaje}", True, blanco)
            pantalla.blit(texto, [ancho / 4, y_offset])
            y_offset += 30
    else:
        mensaje("No hay puntajes guardados.", blanco)
    pygame.display.update()
    time.sleep(5)

def mostrar_puntaje(puntos):
    valor = fuente.render("Puntos: " + str(puntos), True, blanco)
    pantalla.blit(valor, [0, 0])

def dibujar_serpiente(tam_bloque, lista_serpiente):
    for x in lista_serpiente:
        pygame.draw.rect(pantalla, verde, [x[0], x[1], tam_bloque, tam_bloque])

def mensaje(msg, color):
    fuente_mensaje = pygame.font.SysFont(None, 20)
    texto = fuente_mensaje.render(msg, True, color)
    pantalla.blit(texto, [ancho / 6, alto / 3])

def reiniciar_juego():
    x1 = ancho / 2
    y1 = alto / 2
    x1_cambio = 0
    y1_cambio = 0
    lista_serpiente = []
    longitud_serpiente = 1
    manzana_x = round(random.randrange(0, ancho - tam_bloque) / 20.0) * 20.0
    manzana_y = round(random.randrange(0, alto - tam_bloque) / 20.0) * 20.0
    puntos = 0
    return x1, y1, x1_cambio, y1_cambio, lista_serpiente, longitud_serpiente, manzana_x, manzana_y, puntos

def ingresar_nombre():
    nombre = ""
    ingresando = True
    pantalla.fill(azul)
    mensaje("Introduce tu nombre: ", blanco)
    pygame.display.update()

    while ingresando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter para confirmar
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:  # Borrar el último carácter
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode

        pantalla.fill(azul)
        mensaje("Introduce tu nombre: " + nombre, blanco)
        pygame.display.update()

    return nombre

def juego():
    game_over = False
    game_close = False
    puntaje_guardado = False  # Flag para controlar que solo se guarde una vez el puntaje

    x1, y1, x1_cambio, y1_cambio, lista_serpiente, longitud_serpiente, manzana_x, manzana_y, puntos = reiniciar_juego()

    reloj = pygame.time.Clock()

    # Inicialización del joystick (si está conectado)
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    while not game_over:

        while game_close == True:
            pantalla.fill(azul)
            mensaje("¡Perdiste! Presiona Q para salir, R para reiniciar, P para Puntajes", rojo)
            mostrar_puntaje(puntos)
            pygame.display.update()

            if not puntaje_guardado:  # Guarda el puntaje solo la primera vez que entra en game_close
                nombre = ingresar_nombre()
                guardar_puntaje(nombre, puntos)
                puntaje_guardado = True  # Evita guardar múltiples veces

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if evento.key == pygame.K_r or (joystick and joystick.get_button(1)):  # Tecla R o botón B
                        x1, y1, x1_cambio, y1_cambio, lista_serpiente, longitud_serpiente, manzana_x, manzana_y, puntos = reiniciar_juego()
                        game_close = False
                        puntaje_guardado = False  # Reinicia el flag para la próxima partida
                    if evento.key == pygame.K_p or (joystick and joystick.get_button(1)):  # Tecla P o botón Menos (-)
                        mostrar_mejores_puntajes()
                    if joystick and joystick.get_button(9):  # Botón Más (+)
                        game_over = True
                        game_close = False
                    # Esto va dentro del bucle principal, donde ya manejas eventos del joystick.
                    if joystick:
                        for i in range(joystick.get_numbuttons()):
                            if joystick.get_button(i):
                                print(f"Botón {i} presionado")

        #Controles Teclado
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_cambio = -tam_bloque
                    y1_cambio = 0
                elif evento.key == pygame.K_RIGHT:
                    x1_cambio = tam_bloque
                    y1_cambio = 0
                elif evento.key == pygame.K_UP:
                    y1_cambio = -tam_bloque
                    x1_cambio = 0
                elif evento.key == pygame.K_DOWN:
                    y1_cambio = tam_bloque
                    x1_cambio = 0

        # Control del joystick(Switch)
        if joystick:
            eje_x = joystick.get_axis(0)
            eje_y = joystick.get_axis(1)

            if eje_x < -0.5:  # Mover a la izquierda
                x1_cambio = -tam_bloque
                y1_cambio = 0
            elif eje_x > 0.5:  # Mover a la derecha
                x1_cambio = tam_bloque
                y1_cambio = 0
            elif eje_y < -0.5:  # Mover hacia arriba
                y1_cambio = -tam_bloque
                x1_cambio = 0
            elif eje_y > 0.5:  # Mover hacia abajo
                y1_cambio = tam_bloque
                x1_cambio = 0

        if x1 >= ancho or x1 < 0 or y1 >= alto or y1 < 0:
            game_close = True
        x1 += x1_cambio
        y1 += y1_cambio
        pantalla.fill(azul)
        pygame.draw.rect(pantalla, rojo, [manzana_x, manzana_y, tam_bloque, tam_bloque])
        cabeza_serpiente = []
        cabeza_serpiente.append(x1)
        cabeza_serpiente.append(y1)
        lista_serpiente.append(cabeza_serpiente)
        if len(lista_serpiente) > longitud_serpiente:
            del lista_serpiente[0]

        for x in lista_serpiente[:-1]:
            if x == cabeza_serpiente:
                game_close = True

        dibujar_serpiente(tam_bloque, lista_serpiente)
        mostrar_puntaje(puntos)

        pygame.display.update()

        if x1 == manzana_x and y1 == manzana_y:
            manzana_x = round(random.randrange(0, ancho - tam_bloque) / 20.0) * 20.0
            manzana_y = round(random.randrange(0, alto - tam_bloque) / 20.0) * 20.0
            longitud_serpiente += 1
            puntos += 100

        reloj.tick(velocidad)

    pygame.quit()
    quit()

juego()
