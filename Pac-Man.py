import pygame
import time
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((448, 576))
pygame.display.set_caption("Pac-Man")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Mapa del juego (simplificado)
original_game_map = [
    "####################",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#*#.............#*#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.###.#.###.####",
    "####.#.......#.####",
    "####.#.## ##.#.####",
    "#.....#     #.....#",
    "####.# #####.#.####",
    "####.#.......#.####",
    "####.#.#####.#.####",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#*#....#...#....#*#",
    "#.####.#.#.#.####.#",
    "#.................#",
    "####################"
]

# Funciones para manejar el mapa
def get_points():
    points = []
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == '.':
                points.append((x, y))
    return points

def update_map(x, y):
    # Actualizar el mapa para que el punto desaparezca
    row = list(game_map[y])
    row[x] = ' '
    game_map[y] = ''.join(row)

def restore_map():
    global game_map
    game_map = [list(row) for row in original_game_map]

def save_time(name, time_elapsed):
    with open('Tiempo Pacman.txt', 'a') as file:
        file.write(f"{name}: {time_elapsed}s\n")

def show_game_over_menu(time_elapsed):
    font = pygame.font.SysFont(None, 36)
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    retry_text = font.render("Press R to Retry", True, WHITE)
    high_scores_text = font.render("Press T for Best Times", True, WHITE)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 100))
    screen.blit(retry_text, (screen.get_width() // 2 - retry_text.get_width() // 2, 200))
    screen.blit(high_scores_text, (screen.get_width() // 2 - high_scores_text.get_width() // 2, 250))
    screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 300))
    time_text = font.render(f"Your Time: {time_elapsed}s", True, WHITE)
    screen.blit(time_text, (screen.get_width() // 2 - time_text.get_width() // 2, 150))
    pygame.display.flip()

def show_high_scores():
    font = pygame.font.SysFont(None, 36)
    screen.fill(BLACK)
    try:
        with open('Tiempo Pacman.txt', 'r') as file:
            high_scores = file.readlines()
    except FileNotFoundError:
        high_scores = []

    if high_scores:
        high_scores_text = font.render("High Scores:", True, WHITE)
        screen.blit(high_scores_text, (10, 10))
        for i, score in enumerate(high_scores):
            score_text = font.render(f"{i + 1}. {score.strip()}", True, WHITE)
            screen.blit(score_text, (10, 50 + i * 30))
    else:
        no_scores_text = font.render("No Scores Available", True, WHITE)
        screen.blit(no_scores_text, (10, 50))
    
    pygame.display.flip()
    wait_for_keypress()

def wait_for_keypress():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_t:
                    show_high_scores()

def get_player_name():
    font = pygame.font.SysFont(None, 36)
    input_box = pygame.Rect(100, 350, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    text = ''
    active = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

        screen.fill(BLACK)
        prompt_text = font.render("Ingrese un nombre:", True, WHITE)
        screen.blit(prompt_text, (100, 300))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

# Clases del juego
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.powered_up = False
        self.powerup_time = 0

    def move(self, dx, dy):
        if game_map[self.y + dy][self.x + dx] != '#':
            self.x += dx
            self.y += dy

    def draw(self):
        color = GREEN if self.powered_up else YELLOW
        pygame.draw.circle(screen, color, (self.x * 24 + 12, self.y * 24 + 12), 12)

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.respawn_time = 0

    def move(self):
        if self.alive:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            dx, dy = random.choice(directions)
            if game_map[self.y + dy][self.x + dx] != '#':
                self.x += dx
                self.y += dy

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, RED, (self.x * 24, self.y * 24, 24, 24))

def main():
    global start_time
    clock = pygame.time.Clock()
    running = True

    while running:
        # Inicializar el estado del juego
        restore_map()  # Restaurar el mapa original de puntos
        player = Player(9, 15)
        ghosts = [Ghost(9, 7), Ghost(10, 7)]
        points = get_points()  # Lista de puntos en el mapa
        start_time = time.time()  # Tiempo de inicio

        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_running = False
                    elif event.key == pygame.K_t:
                        show_high_scores()
                    elif event.key == pygame.K_q:
                        running = False
                        game_running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(-1, 0)
            if keys[pygame.K_RIGHT]:
                player.move(1, 0)
            if keys[pygame.K_UP]:
                player.move(0, -1)
            if keys[pygame.K_DOWN]:
                player.move(0, 1)

            # Actualizar estado de power-up
            if player.powered_up and time.time() - player.powerup_time > 20:
                player.powered_up = False

            # Mover fantasmas
            for ghost in ghosts:
                if not ghost.alive and time.time() - ghost.respawn_time > 15:
                    ghost.alive = True
                ghost.move()

            # Colisiones con fantasmas
            for ghost in ghosts:
                if player.x == ghost.x and player.y == ghost.y:
                    if player.powered_up:
                        ghost.alive = False
                        ghost.respawn_time = time.time()
                    else:
                        game_running = False

            # Colisiones con puntos
            if (player.x, player.y) in points:
                points.remove((player.x, player.y))
                update_map(player.x, player.y)  # Actualiza el mapa
                if len(points) == 0:
                    game_running = False

            # Contador de tiempo
            elapsed_time = int(time.time() - start_time)

            # Dibujar mapa
            screen.fill(BLACK)
            for y, row in enumerate(game_map):
                for x, cell in enumerate(row):
                    if cell == '#':
                        pygame.draw.rect(screen, BLUE, (x * 24, y * 24, 24, 24))
                    elif cell == '.':
                        pygame.draw.circle(screen, WHITE, (x * 24 + 12, y * 24 + 12), 6)  # Punto pequeño

            # Dibujar jugador y fantasmas
            player.draw()
            for ghost in ghosts:
                ghost.draw()

            # Mostrar contador de tiempo
            font = pygame.font.SysFont(None, 36)
            time_text = font.render(f"Time: {elapsed_time}s", True, WHITE)
            screen.blit(time_text, (10, 552))  # Ubicación en la parte inferior de la pantalla

            pygame.display.flip()
            clock.tick(30)

        if len(points) == 0:  # Si ganó
            name = get_player_name()
            save_time(name, elapsed_time)
        
        # Mostrar el menú de fin de juego
        show_game_over_menu(elapsed_time)
        wait_for_keypress()

    pygame.quit()

if __name__ == "__main__":
    main()
