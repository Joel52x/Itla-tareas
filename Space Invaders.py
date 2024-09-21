import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
fire_red = (255, 69, 0)

# Configuración del jugador
player_size = 50
player_speed = 5

# Configuración del disparo
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Configuración de los invasores
invader_size = 50
invader_speed = 2
invaders = []

# Fuentes
font = pygame.font.Font(None, 74)
input_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 36)  # Fuente para las instrucciones

# Función para crear un nuevo invasor
def create_invader():
    x = random.randint(0, screen_width - invader_size)
    y = random.randint(-100, -40)
    invaders.append([x, y])

# Función para dibujar el jugador
def draw_player(x, y):
    pygame.draw.rect(screen, green, (x, y, player_size, player_size))

# Función para dibujar los disparos
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, fire_red, (bullet[0], bullet[1], bullet_width, bullet_height))

# Función para dibujar los invasores
def draw_invaders(invaders):
    for invader in invaders:
        pygame.draw.rect(screen, white, (invader[0], invader[1], invader_size, invader_size))

# Función para detectar colisiones
def detect_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Función para guardar puntajes
def save_score(player_name, score):
    with open("space_invaders_scores.txt", "a") as file:
        file.write(f"{player_name}: {score}\n")

# Función para mostrar los mejores puntajes
def show_high_scores():
    try:
        with open("space_invaders_scores.txt", "r") as file:
            scores = file.readlines()
        scores = [score.strip() for score in scores]
        scores.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)  # Ordenar por puntaje

        screen.fill(black)
        y_offset = 150
        for idx, score in enumerate(scores[:5]):  # Mostrar los primeros 5 puntajes
            score_text = input_font.render(f"{idx + 1}. {score}", True, white)
            screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, y_offset))
            y_offset += 50
        pygame.display.flip()
        pygame.time.delay(3000)  # Espera para que se puedan ver los puntajes
    except FileNotFoundError:
        print("No high scores available.")

# Función principal del juego
def main():
    clock = pygame.time.Clock()
    score = 0
    game_over = False
    player_name = ""
    input_active = True

    player_x = screen_width // 2 - player_size // 2
    player_y = screen_height - player_size - 10

    # Pantalla de ingreso de nombre
    while input_active:
        screen.fill(black)
        input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 200, 40)
        pygame.draw.rect(screen, white, input_box, 2)

        text_surface = input_font.render(player_name, True, white)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        prompt_text = font.render("Introduce tu nombre", True, white)
        screen.blit(prompt_text, (screen_width // 2 - prompt_text.get_width() // 2, screen_height // 2 - prompt_text.get_height() // 2 - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        pygame.display.flip()
        clock.tick(30)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
            player_x += player_speed
        if keys[pygame.K_UP]:
            bullets.append([player_x + player_size // 2 - bullet_width // 2, player_y])

        screen.fill(black)

        draw_player(player_x, player_y)

        # Actualizar balas
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        draw_bullets(bullets)

        # Crear invasores aleatoriamente
        if random.randint(1, 20) == 1:
            create_invader()

        # Actualizar la posición de los invasores
        for invader in invaders[:]:
            invader[1] += invader_speed
            if invader[1] > screen_height:
                invaders.remove(invader)

        # Detectar colisiones entre balas e invasores
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            for invader in invaders[:]:
                invader_rect = pygame.Rect(invader[0], invader[1], invader_size, invader_size)
                if detect_collision(bullet_rect, invader_rect):
                    bullets.remove(bullet)
                    invaders.remove(invader)
                    score += 10
                    break

        # Detectar colisiones entre el jugador e invasores
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for invader in invaders:
            invader_rect = pygame.Rect(invader[0], invader[1], invader_size, invader_size)
            if detect_collision(player_rect, invader_rect):
                game_over = True
                save_score(player_name, score)
                break

        draw_invaders(invaders)

        pygame.display.flip()
        clock.tick(60)

    # Mensaje de fin de juego y opciones
    while True:
        screen.fill(black)
        game_over_text = font.render("Game Over!", True, white)
        score_text = font.render(f"Tu score: {score}", True, white)
        name_text = font.render(f"Jugador: {player_name}", True, white)

        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
        screen.blit(name_text, (screen_width // 2 - name_text.get_width() // 2, screen_height // 2 + 100))

        # Instrucciones
        instructions_text = small_font.render("Presiona P para ver los puntajes, Q para salir, R para reiniciar", True, white)
        screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, screen_height // 2 + 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Cerrar el juego
                    pygame.quit()
                    return
                if event.key == pygame.K_r:  # Reiniciar el juego
                    main()
                if event.key == pygame.K_p:  # Mostrar los mejores puntajes
                    show_high_scores()

if __name__ == "__main__":
    main()
