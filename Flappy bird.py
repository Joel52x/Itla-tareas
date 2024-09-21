import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

# Dimensiones de la ventana
ancho_ventana = 400
alto_ventana = 600
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption('Flappy Bird')

# Reloj para controlar la velocidad de fotogramas
reloj = pygame.time.Clock()

# Fuente para el puntaje
fuente = pygame.font.SysFont(None, 35)

# Guardar puntaje en archivo de texto
def guardar_puntaje(nombre, puntos):
    with open("puntajes Bird.txt", "a") as archivo:
        archivo.write(f"{nombre}: {puntos}\n")

# Mostrar puntajes más altos
def mostrar_mejores_puntajes():
    try:
        with open("puntajes Bird.txt", "r") as archivo:
            puntajes = archivo.readlines()
            puntajes = [linea.strip() for linea in puntajes if linea.strip()]
            puntajes = [linea.split(": ") for linea in puntajes]
            puntajes = [(nombre, int(puntaje)) for nombre, puntaje in puntajes]
            puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)[:5]
    except FileNotFoundError:
        puntajes_ordenados = []

    pantalla.fill(azul)
    y_offset = 50
    if puntajes_ordenados:
        for i, (nombre, puntaje) in enumerate(puntajes_ordenados, start=1):
            texto = fuente.render(f"{i}. {nombre}: {puntaje}", True, blanco)
            pantalla.blit(texto, [ancho_ventana / 4, y_offset])
            y_offset += 30
    else:
        texto = fuente.render("No hay puntajes guardados", True, blanco)
        pantalla.blit(texto, [ancho_ventana / 4, alto_ventana / 2])

    pygame.display.update()
    time.sleep(5)

# Función para mostrar puntaje
def mostrar_puntaje(puntos):
    valor = fuente.render("Puntaje: " + str(puntos), True, blanco)
    pantalla.blit(valor, [10, 10])

# Ingresar nombre en pantalla
def ingresar_nombre():
    nombre = ""
    ingresando = True
    pantalla.fill(azul)
    texto = fuente.render("Introduce tu nombre: ", True, blanco)
    pantalla.blit(texto, [ancho_ventana / 6, alto_ventana / 3])
    pygame.display.update()

    while ingresando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += evento.unicode

        pantalla.fill(azul)
        texto = fuente.render(f"Introduce tu nombre: {nombre}", True, blanco)
        pantalla.blit(texto, [ancho_ventana / 6, alto_ventana / 3])
        pygame.display.update()

    return nombre

# Función de menú post-partida
def menu_post_partida():
    pantalla.fill(azul)
    texto = fuente.render("Presiona R para reiniciar", True, blanco)
    pantalla.blit(texto, [ancho_ventana / 6, alto_ventana / 3])
    texto = fuente.render("Presiona P para puntajes", True, blanco)
    pantalla.blit(texto, [ancho_ventana / 6, alto_ventana / 2.5])
    texto = fuente.render("Presiona Q para salir", True, blanco)
    pantalla.blit(texto, [ancho_ventana / 6, alto_ventana / 2])
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    juego()  # Reiniciar el juego
                if evento.key == pygame.K_p:
                    mostrar_mejores_puntajes()  # Mostrar puntajes
                    menu_post_partida()  # Volver al menú después de mostrar puntajes
                if evento.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Función principal del juego
def juego():
    game_over = False
    puntos = 0

    # Posiciones del pájaro
    pos_x = 50
    pos_y = alto_ventana // 2
    velocidad_y = 0
    gravedad = 1

    # Tuberías
    tuberias = []
    tuberia_ancho = 70
    tuberia_velocidad = 5
    tuberia_espacio = 150
    tuberia_frecuencia = 1500  # Cada 1500 ms aparece una nueva tubería
    tiempo_ultima_tuberia = pygame.time.get_ticks()

    def crear_tuberia():
        altura = random.randint(100, 400)
        return {'x': ancho_ventana, 'y': altura}

    while not game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocidad_y = -10

        # Mover al pájaro
        velocidad_y += gravedad
        pos_y += velocidad_y

        # Verificar colisión con el suelo o el techo
        if pos_y > alto_ventana or pos_y < 0:
            game_over = True

        # Crear nuevas tuberías
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultima_tuberia > tuberia_frecuencia:
            tuberias.append(crear_tuberia())
            tiempo_ultima_tuberia = tiempo_actual

        # Mover las tuberías
        for tuberia in tuberias:
            tuberia['x'] -= tuberia_velocidad

        # Eliminar tuberías fuera de la pantalla
        tuberias = [tuberia for tuberia in tuberias if tuberia['x'] > -tuberia_ancho]

        # Verificar colisión con las tuberías
        for tuberia in tuberias:
            if pos_x + 40 > tuberia['x'] and pos_x < tuberia['x'] + tuberia_ancho:
                if pos_y < tuberia['y'] - tuberia_espacio // 2 or pos_y > tuberia['y'] + tuberia_espacio // 2:
                    game_over = True

        # Aumentar el puntaje si el pájaro pasa una tubería
        if len(tuberias) > 0 and tuberias[0]['x'] < pos_x and not tuberias[0].get('pasada'):
            puntos += 100
            tuberias[0]['pasada'] = True

        # Dibujar todo
        pantalla.fill(negro)

        # Dibujar pájaro
        pygame.draw.rect(pantalla, rojo, [pos_x, pos_y, 40, 40])

        # Dibujar tuberías
        for tuberia in tuberias:
            pygame.draw.rect(pantalla, verde, [tuberia['x'], 0, tuberia_ancho, tuberia['y'] - tuberia_espacio // 2])
            pygame.draw.rect(pantalla, verde, [tuberia['x'], tuberia['y'] + tuberia_espacio // 2, tuberia_ancho, alto_ventana])

        # Mostrar puntaje
        mostrar_puntaje(puntos)

        pygame.display.update()
        reloj.tick(30)

    # Al finalizar el juego, pedir nombre y guardar puntaje dentro de la ventana
    nombre = ingresar_nombre()
    guardar_puntaje(nombre, puntos)
    
    # Mostrar el menú para reiniciar, salir o ver los puntajes
    menu_post_partida()

juego()
