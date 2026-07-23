import pygame
import random
import sys

pygame.init()

CELL = 20
WIDTH, HEIGHT = 600, 400
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 24)

snake = [(WIDTH // 2, HEIGHT // 2)]
direction = (CELL, 0)
food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
score = 0
alive = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    if alive:
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if head in snake or head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            alive = False
        else:
            snake.insert(0, head)
            if head == food:
                score += 1
                food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            else:
                snake.pop()

    screen.fill((0, 0, 0))
    for seg in snake:
        pygame.draw.rect(screen, (0, 200, 0), (*seg, CELL, CELL))
    pygame.draw.rect(screen, (200, 0, 0), (*food, CELL, CELL))
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    if not alive:
        screen.blit(font.render("GAME OVER - Press R to restart", True, (255, 255, 255)), (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()
    clock.tick(FPS)

    if not alive:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                snake = [(WIDTH // 2, HEIGHT // 2)]
                direction = (CELL, 0)
                food = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
                score = 0
                alive = True
