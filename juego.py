import pygame
import numpy as np

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de raquetas y pelota
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 10
paddle_speed = 5
ball_speed = np.array([4, 4])

# Posiciones iniciales
left_paddle = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_pos = np.array([WIDTH // 2, HEIGHT // 2])

# Puntuación
left_score = 0
right_score = 0
font = pygame.font.Font(None, 36)

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    # Eventos de cierre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de raquetas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.move_ip(0, paddle_speed)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.move_ip(0, paddle_speed)

    # Movimiento de la pelota
    ball_pos += ball_speed

    # Colisión con paredes
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Colisión con raquetas
    if left_paddle.collidepoint(ball_pos[0] - BALL_RADIUS, ball_pos[1]):
        ball_speed[0] = -ball_speed[0]
    elif right_paddle.collidepoint(ball_pos[0] + BALL_RADIUS, ball_pos[1]):
        ball_speed[0] = -ball_speed[0]

    # Puntuación
    if ball_pos[0] < 0:
        right_score += 1
        ball_pos = np.array([WIDTH // 2, HEIGHT // 2])
        ball_speed = np.array([4 * (-1 if right_score % 2 == 0 else 1), 4])
    elif ball_pos[0] > WIDTH:
        left_score += 1
        ball_pos = np.array([WIDTH // 2, HEIGHT // 2])
        ball_speed = np.array([4 * (-1 if left_score % 2 == 0 else 1), 4])

    # Dibujar en pantalla
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.circle(screen, WHITE, ball_pos.astype(int), BALL_RADIUS)

    # Dibujar puntuación
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (3 * WIDTH // 4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
