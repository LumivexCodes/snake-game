import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

# Clock
clock = pygame.time.Clock()

# Time settings for smooth movement
MOVE_INTERVAL = 150  # milliseconds per move

# --- Helper functions ---
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def button(surface, color, x, y, w, h, text, text_color):
    pygame.draw.rect(surface, color, (x, y, w, h))
    draw_text(text, small_font, text_color, surface, x + w // 2, y + h // 2)
    return pygame.Rect(x, y, w, h)


def spawn_food(snake_pos):
    while True:
        pos = [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
               random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]
        if pos not in snake_pos:
            return pos


# --- Main Menu ---
def main_menu():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Snake Game", font, GREEN, screen, WIDTH // 2, HEIGHT // 4)

        play_button = button(screen, GRAY, WIDTH // 2 - 75, HEIGHT // 2 - 30, 150, 50, "Play", BLACK)
        howto_button = button(screen, GRAY, WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50, "How To Play", BLACK)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    game_loop()
                if howto_button.collidepoint(event.pos):
                    how_to_play()


# --- How To Play Screen ---
def how_to_play():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("How To Play", font, BLUE, screen, WIDTH // 2, HEIGHT // 6)
        instructions = [
            "Use arrow keys to move the snake.",
            "Eat red apples to grow.",
            "Don't hit the walls or yourself.",
            "Press ESC to go back."
        ]
        for i, line in enumerate(instructions):
            draw_text(line, small_font, WHITE, screen, WIDTH // 2, HEIGHT // 3 + i * 30)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


# --- Game Over Screen ---
def game_over(score):
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("GAME OVER", font, RED, screen, WIDTH // 2, HEIGHT // 3)
        draw_text(f"Score: {score}", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to return to Menu", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


# --- Snake Game Loop ---
def game_loop():
    snake_pos = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"
    change_to = direction

    food_pos = spawn_food(snake_pos)
    score = 0
    running = True

    last_move_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Move snake only if MOVE_INTERVAL has passed
        if current_time - last_move_time > MOVE_INTERVAL:
            direction = change_to
            head_x, head_y = snake_pos[0]
            if direction == "UP": head_y -= CELL_SIZE
            if direction == "DOWN": head_y += CELL_SIZE
            if direction == "LEFT": head_x -= CELL_SIZE
            if direction == "RIGHT": head_x += CELL_SIZE
            new_head = [head_x, head_y]

            if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in snake_pos:
                game_over(score)
                running = False
                continue

            snake_pos.insert(0, new_head)
            if new_head == food_pos:
                score += 1
                food_pos = spawn_food(snake_pos)
            else:
                snake_pos.pop()

            last_move_time = current_time

        # Draw everything
        screen.fill(BLACK)
        for block in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

        draw_text(f"Score: {score}", small_font, WHITE, screen, 60, 20)

        pygame.display.update()
        clock.tick(60)  # keep FPS high but movement controlled by MOVE_INTERVAL


# --- Start Game ---
main_menu()
