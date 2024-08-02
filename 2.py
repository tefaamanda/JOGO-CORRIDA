import pygame
import sys
import random
import time

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Turbo Rush")

# Cores
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'GREEN': (0, 255, 0),
    'YELLOW': (255, 255, 0), # Cor amarela para os pontos
    'PURPLE': (128, 0, 128),  # Cor roxa para os pontos
    'PINK': (255, 192, 203),  # Cor rosa para o triângulo
    'GRAY': (169, 169, 169),
}

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Turbo Rush")

# Carregar e redimensionar imagens
player1_image = pygame.image.load('caroasu.png')
player2_image = pygame.image.load('carovermei.png')
obstacle_image = pygame.image.load('26130-removebg-preview.png')
circle_yellow_image = pygame.image.load('pilha.png')
circle_purple_image = pygame.image.load('gaso.png')
triangle_pink_image = pygame.image.load('—Pngtree—yellow hard pattern cartoon stone_4492648.png')

# Ajustar o tamanho das imagens
player1_image = pygame.transform.scale(player1_image, (80, 80))
player2_image = pygame.transform.scale(player2_image, (80, 80))
obstacle_image = pygame.transform.scale(obstacle_image, (100, 100))
circle_yellow_image = pygame.transform.scale(circle_yellow_image, (50, 50))
circle_purple_image = pygame.transform.scale(circle_purple_image, (50, 50))
triangle_pink_image = pygame.transform.scale(triangle_pink_image, (100, 100))

# Definições iniciais
player1_x, player1_y = 100, screen_height // 2
player2_x, player2_y = 200, screen_height // 2
player1_speed = 5
player2_speed = 5
player_speed = 5
player1_speed_time = 0
player2_speed_time = 0
player1_score = 0
player2_score = 0
race_duration = 30000  # 30 segundos
start_time = pygame.time.get_ticks()
race_over = False

def start_screen():
    running = True
    selected_color = None
    selected_map = None
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_color and selected_map:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x_offset = 50
                for color in COLORS.keys():
                    if pygame.Rect(x_offset, 200, 50, 50).collidepoint(mouse_x, mouse_y):
                        selected_color = color
                    x_offset += 70
                y_offset = 350
                for map_time in ["manhã", "tarde", "noite"]:
                    text_rect = pygame.Rect(50, y_offset, small_font.size(map_time.capitalize())[0], small_font.get_height())
                    if text_rect.collidepoint(mouse_x, mouse_y):
                        selected_map = map_time
                    y_offset += 50

        screen.fill((0, 0, 0))
        title_text = font.render("Turbo Rush", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

        color_text = small_font.render("Selecione a Cor do Veículo:", True, (255, 255, 255))
        screen.blit(color_text, (50, 150))
        x_offset = 50
        for color in COLORS.keys():
            pygame.draw.rect(screen, COLORS[color], (x_offset, 200, 50, 50))
            if selected_color == color:
                pygame.draw.rect(screen, (255, 255, 255), (x_offset, 200, 50, 50), 2)
            x_offset += 70

        map_text = small_font.render("Selecione a Hora do Dia:", True, (255, 255, 255))
        screen.blit(map_text, (50, 300))
        map_times = ["manhã", "tarde", "noite"]
        y_offset = 350
        for map_time in map_times:
            text = small_font.render(map_time.capitalize(), True, (255, 255, 255))
            screen.blit(text, (50, y_offset))
            if selected_map == map_time:
                pygame.draw.rect(screen, (255, 255, 255), (40, y_offset - 10, text.get_width() + 20, text.get_height() + 10), 2)
            y_offset += 50

        start_text = small_font.render("Pressione ENTER para começar", True, (255, 255, 255))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 500))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Posições iniciais dos jogadores
player1_start_x = screen_width // 4
player1_start_y = screen_height - 50
player2_start_x = 3 * screen_width // 4
player2_start_y = screen_height - 50

# Velocidade de movimento dos jogadores
player_speed = 5

# Fonte para a pontuação e para o texto do vencedor
font = pygame.font.Font(None, 74)
winner_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 50)

# Temporizador da corrida
race_duration = 20000  # duração da corrida em milissegundos (20 segundos)

def reset_game():
    global player1_x, player1_y, player2_x, player2_y
    global player1_score, player2_score
    global obstacles, circles_yellow, circles_purple, triangles
    global start_time, race_over, last_obstacle_spawn, last_circle_yellow_spawn, last_circle_purple_spawn, last_triangle_spawn
    global player1_speed, player2_speed, player1_speed_time, player2_speed_time

    # Posições iniciais dos jogadores
    player1_x, player1_y = player1_start_x, player1_start_y
    player2_x, player2_y = player2_start_x, player2_start_y

    # Pontuação
    player1_score = 0
    player2_score = 0

    # Velocidade dos jogadores e temporizadores de velocidade
    player1_speed = player_speed
    player2_speed = player_speed
    player1_speed_time = 0
    player2_speed_time = 0

    # Listas de obstáculos, círculos e triângulos
    obstacles = []
    circles_yellow = []
    circles_purple = []
    triangles = []

    # Início do temporizador da corrida
    start_time = pygame.time.get_ticks()
    race_over = False

    # Inicializar tempos de spawn
    last_obstacle_spawn = start_time
    last_circle_yellow_spawn = start_time
    last_circle_purple_spawn = start_time
    last_triangle_spawn = start_time

reset_game()

# Função para criar um novo obstáculo
def create_obstacle():
    x = random.randint(0, screen_width - 50)
    y = 0
    return pygame.Rect(x, y, 50, 50)

# Função para criar um novo círculo amarelo
def create_circle_yellow():
    x = random.randint(0, screen_width - 30)
    y = 0
    return pygame.Rect(x, y, 30, 30)

# Função para criar um novo círculo roxo
def create_circle_purple():
    x = random.randint(0, screen_width - 30)
    y = 0
    return pygame.Rect(x, y, 30, 30)

# Função para criar um novo triângulo rosa
def create_triangle():
    x = random.randint(0, screen_width - 30)
    y = 0
    return pygame.Rect(x, y, 30, 30)

# Função para desenhar o triângulo rosa
def draw_triangle(surface, color, rect):
    points = [
        (rect.centerx, rect.top),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ]
    pygame.draw.polygon(surface, color, points)

# Função principal do jogo
def game_loop():
    global player1_x, player1_y, player2_x, player2_y
    global player1_score, player2_score
    global obstacles, circles_yellow, circles_purple, triangles
    global start_time, race_over, last_obstacle_spawn, last_circle_yellow_spawn, last_circle_purple_spawn, last_triangle_spawn
    global player1_speed, player2_speed, player1_speed_time, player2_speed_time

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and race_over:
                mouse_x, mouse_y = event.pos
                if button_rect.collidepoint(mouse_x, mouse_y):
                    reset_game()

        if not race_over:
            # Movimentação dos jogadores
            keys = pygame.key.get_pressed()

            # Movimento do jogador 1
            if keys[pygame.K_a]:
                player1_x -= player1_speed
            if keys[pygame.K_d]:
                player1_x += player1_speed
            if keys[pygame.K_w]:
                player1_y -= player1_speed
            if keys[pygame.K_s]:
                player1_y += player1_speed

            # Movimento do jogador 2
            if keys[pygame.K_LEFT]:
                player2_x -= player2_speed
            if keys[pygame.K_RIGHT]:
                player2_x += player2_speed
            if keys[pygame.K_UP]:
                player2_y -= player2_speed
            if keys[pygame.K_DOWN]:
                player2_y += player2_speed

            # Limitar o movimento dos jogadores para dentro da tela
            player1_x = max(0, min(player1_x, screen_width - 50))
            player1_y = max(50, min(player1_y, screen_height - 50))  # Começa a partir da linha de chegada (y=50)

            player2_x = max(0, min(player2_x, screen_width - 50))
            player2_y = max(50, min(player2_y, screen_height - 50))  # Começa a partir da linha de chegada (y=50)

            # Adicionar novos obstáculos
            current_time = pygame.time.get_ticks()
            if current_time - last_obstacle_spawn > 500:
                obstacles.append(create_obstacle())
                last_obstacle_spawn = current_time

            # Adicionar novos círculos amarelos
            if current_time - last_circle_yellow_spawn > 3000:
                circles_yellow.append(create_circle_yellow())
                last_circle_yellow_spawn = current_time

            # Adicionar novos círculos roxos
            if current_time - last_circle_purple_spawn > 5000:
                circles_purple.append(create_circle_purple())
                last_circle_purple_spawn = current_time

            # Adicionar novos triângulos rosas
            if current_time - last_triangle_spawn > 7000:
                triangles.append(create_triangle())
                last_triangle_spawn = current_time

            # Mover os obstáculos
            for obstacle in obstacles:
                obstacle.y += 5

            # Mover os círculos amarelos
            for circle in circles_yellow:
                circle.y += 5

            # Mover os círculos roxos
            for circle in circles_purple:
                circle.y += 5

            # Mover os triângulos rosas
            for triangle in triangles:
                triangle.y += 5

            # Remover obstáculos, círculos e triângulos que saíram da tela
            obstacles = [obstacle for obstacle in obstacles if obstacle.y < screen_height]
            circles_yellow = [circle for circle in circles_yellow if circle.y < screen_height]
            circles_purple = [circle for circle in circles_purple if circle.y < screen_height]
            triangles = [triangle for triangle in triangles if triangle.y < screen_height]

            # Verificar colisões com os obstáculos
            player1_rect = pygame.Rect(player1_x, player1_y, 50, 50)
            player2_rect = pygame.Rect(player2_x, player2_y, 50, 50)

            for obstacle in obstacles:
                if player1_rect.colliderect(obstacle):
                    player1_score = max(0, player1_score - 1)  # Reduz um ponto
                    player1_x, player1_y = player1_start_x, player1_start_y
                if player2_rect.colliderect(obstacle):
                    player2_score = max(0, player2_score - 1)  # Reduz um ponto
                    player2_x, player2_y = player2_start_x, player2_start_y

            # Verificar colisões com os círculos amarelos e roxos
            for circle in circles_yellow:
                if player1_rect.colliderect(circle) and player2_rect.colliderect(circle):
                    player1_score += 1
                    player2_score += 1
                    circles_yellow.remove(circle)
                elif player1_rect.colliderect(circle):
                    player1_score += 1
                    circles_yellow.remove(circle)
                elif player2_rect.colliderect(circle):
                    player2_score += 1
                    circles_yellow.remove(circle)

            for circle in circles_purple:
                if player1_rect.colliderect(circle) and player2_rect.colliderect(circle):
                    player1_score += 2
                    player2_score += 2
                    circles_purple.remove(circle)
                elif player1_rect.colliderect(circle):
                    player1_score += 2
                    circles_purple.remove(circle)
                elif player2_rect.colliderect(circle):
                    player2_score += 2
                    circles_purple.remove(circle)

            # Verificar colisões com os triângulos rosas
            for triangle in triangles:
                if player1_rect.colliderect(triangle):
                    player1_score = max(0, player1_score - 1)  # Reduz um ponto
                    player1_speed *= 0.5
                    player1_speed_time = current_time
                    triangles.remove(triangle)
                if player2_rect.colliderect(triangle):
                    player2_score = max(0, player2_score - 1)  # Reduz um ponto
                    player2_speed *= 0.5
                    player2_speed_time = current_time
                    triangles.remove(triangle)

            # Reverter a velocidade aumentada após 2 segundos
            if current_time - player1_speed_time > 2000:
                player1_speed = player_speed
            if current_time - player2_speed_time > 2000:
                player2_speed = player_speed

            # Verificar se o tempo da corrida acabou
            if current_time - start_time >= race_duration:
                race_over = True
                if player1_score > player2_score:
                    winner_text = "Player 1 Wins!"
                elif player2_score > player1_score:
                    winner_text = "Player 2 Wins!"
                else:
                    winner_text = "Empatou"

        # Limpar a tela
        screen.fill(COLORS['WHITE'])

        # Desenhar os jogadores
        screen.blit(player1_image, (player1_x, player1_y))
        screen.blit(player2_image, (player2_x, player2_y))

        # Desenhar os obstáculos
        for obstacle in obstacles:
            screen.blit(obstacle_image, obstacle.topleft)

        # Desenhar os círculos amarelos
        for circle in circles_yellow:
            screen.blit(circle_yellow_image, circle.topleft)

        # Desenhar os círculos roxos
        for circle in circles_purple:
            screen.blit(circle_purple_image, circle.topleft)

        # Desenhar os triângulos rosas
        for triangle in triangles:
            screen.blit(triangle_pink_image, triangle.topleft)

        # Desenhar a linha de chegada
        pygame.draw.line(screen, COLORS['BLACK'], (0, 50), (screen_width, 50), 5)

        # Exibir pontuação
        score_text = font.render(f"Player 1: {player1_score}  Player 2: {player2_score}", True, COLORS['BLACK'])
        screen.blit(score_text, (20, 10))

        # Exibir o vencedor e o botão de reinício se a corrida acabou
        if race_over:
            winner_display = winner_font.render(winner_text, True, COLORS['BLACK'])
            screen.blit(winner_display, (
            screen_width // 2 - winner_display.get_width() // 2, screen_height // 2 - winner_display.get_height() // 2))

            button_text = button_font.render("Reiniciar", True, COLORS['BLACK'])
            button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            pygame.draw.rect(screen, COLORS['GRAY'], button_rect.inflate(20, 10))
            screen.blit(button_text, button_rect)

        # Atualizar a tela
        pygame.display.flip()

        # Limitar a 60 frames por segundo
        pygame.time.Clock().tick(60)

    # Sair do Pygame
    pygame.quit()
    sys.exit()

# Chamar a tela inicial antes de iniciar o loop principal do jogo
start_screen()

# Iniciar o loop principal do jogo
game_loop()
 