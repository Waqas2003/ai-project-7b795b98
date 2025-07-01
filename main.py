# file: snake_game/requirements.txt
pygame

# file: snake_game/.gitignore
__pycache__/
venv/

# file: snake_game/snake_game/__init__.py

# file: snake_game/snake_game/config.py
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
SPEED = 10

# file: snake_game/snake_game/models.py
class Snake:
    def __init__(self):
        self.body = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'

    def move(self):
        head = self.body[0]
        if self.direction == 'RIGHT':
            new_head = (head[0] + BLOCK_SIZE, head[1])
        elif self.direction == 'LEFT':
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == 'UP':
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + BLOCK_SIZE)
        self.body.insert(0, new_head)

    def eat(self, food):
        if self.body[0] == food:
            return True
        else:
            self.body.pop()
            return False

class Food:
    def __init__(self):
        self.position = (400, 300)

    def generate(self):
        self.position = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                         random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)

# file: snake_game/snake_game/views.py
import pygame
from .models import Snake, Food
from .config import WIDTH, HEIGHT, BLOCK_SIZE

def draw_snake(snake, screen):
    for pos in snake.body:
        pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food, screen):
    pygame.draw.rect(screen, (255, 0, 0), (food.position[0], food.position[1], BLOCK_SIZE, BLOCK_SIZE))

def game_over(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2 - 18))

# file: snake_game/snake_game/main.py
import pygame
from .models import Snake, Food
from .views import draw_snake, draw_food, game_over
from .config import WIDTH, HEIGHT, SPEED

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    food.generate()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'

        snake.move()
        if snake.eat(food):
            food.generate()
        else:
            if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
                snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT or
                snake.body[0] in snake.body[1:]):
                running = False

        screen.fill((0, 0, 0))
        draw_snake(snake, screen)
        draw_food(food, screen)
        pygame.display.flip()
        clock.tick(SPEED)

    game_over(screen)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()